from pathlib import Path
import xml.etree.ElementTree as ET
from datetime import datetime

import requests

from django.template import Context, Template
from django.conf import settings

from attach.models import MpiMessages


class MpiRegisterAttachMixin(object):
    template_dir = settings.BASE_DIR / "attach/api/templates"
    mixin_template_soap = ""
    mixin_cleaned_data = {}
    pid = None
    attach_id = None

    def mixin_get_data(self):
        template_file = Path(self.template_dir, self.mixin_template_soap)
        with open(template_file) as f:
            template = Template(f.read())
        context = Context(self.mixin_cleaned_data)
        
        return template.render(context)
    
    def mixin_send_request(self):
        url = settings.MPI_REGISTER_ATTACH_URL
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "X-Auth-Token": settings.MPI_TOKEN,
        }
        body = self.mixin_get_data().encode("utf-8")

        mpi_msg = MpiMessages(
            pid=self.pid,
            attach_id=self.attach_id,
            dt_request=datetime.now(),
            mpi_request=self.mixin_get_data().replace(' ', '').replace('\n', ''),
            rguid=self.mixin_cleaned_data['rguid'],
            mpi_service='registerAttach'
        )
        mpi_msg.save()

        try:
            response = requests.post(url, data=body, headers=headers)
            MpiMessages.objects.filter(pk=mpi_msg.pk).update(
                dt_response=datetime.now(),
                mpi_response=response.text
            )
        except requests.exceptions.RequestException as e:
            return {'err_code': '500', 'err_message': 'Сервер ФЕРЗЛ не отвечает.'}
        return response.text
    
    def mixin_mpi_response(self):
        response = self.mixin_send_request()

        if type(response) == dict:
            return response
        
        root = ET.fromstring(response)
        pars = {}
        for child in root.iter("*"):
            if child.tag == "{http://ffoms.ru/types/4.5/commonTypes}code":
                pars["err_code"] = child.text.strip()
            elif child.tag == "{http://ffoms.ru/types/4.5/commonTypes}message":
                pars["err_message"] = child.text.strip()
        return pars