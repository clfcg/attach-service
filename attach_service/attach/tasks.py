from datetime import datetime
import json
import shutil

import dramatiq

from django.conf import settings
from django.db.models import Q, Max

from .models import People, Histlpu, GetViewDataAttachPoll


@dramatiq.actor
def generate_attach_file(op_token, date_query):
    print(f'Начало - {datetime.now()}')

    people_data = People.objects.filter(dbeg__lt=date_query).filter(Q(dstop__gt=date_query) | Q(dstop__isnull=True))
    people_data = people_data.extra(select={"dbeg": "convert(varchar, dbeg, 23)"})

    persona_dict = {} # Данные застрахованного
    attach_dict = {} # Полные данные по прикреплению
    attach_list = [] # 
    for item in people_data[:1000]:
        attach = item.people.filter(lpudt__lt=date_query).filter(Q(lpudx__gt=date_query) | Q(lpudx__isnull=True)).order_by('-lpudt', 'lpudx', '-id')
        if len(attach) > 0:
            persona_dict.clear()
            attach_dict.clear()
            attach = attach[0]

            persona_dict["enp"] = item.enp
            persona_dict["ss"] = item.ss
            persona_dict["polisBegin"] = item.dbeg
            persona_dict["codeSmo"] = item.q

            attach_dict["persona"] = persona_dict
            attach_dict["attachDBeg"] = attach.lpudt.strftime("%Y-%m-%d")
            if attach.lpudx is not None:
                attach_dict["attachDEnd"] = attach.lpudx.strftime("%Y-%m-%d")
            attach_dict["attachCodeMo"] = attach.lpu
            attach_list.append(attach_dict)
        else:
            continue

    file_path = settings.BASE_DIR / 'temp_files'
    file_json_name = file_path / f'{op_token}.json'
    file_xml_name = file_path / f'{op_token}'
    with open(file_json_name, 'w') as f:
        json.dump(attach_list, f, indent=4)

    shutil.make_archive(file_xml_name,'zip',file_path)

    op = GetViewDataAttachPoll.objects.get(op_token=op_token)
    #upload_file = open(file_path / f'{op_token}.zip')
    with open(file_path / f'{op_token}.zip', '+rb') as f:
        op.poll_file.save(f'{op_token}.zip', f)
        op.status = 'COMPLITE'
        op.save()

    print(f'Конец - {datetime.now()}')