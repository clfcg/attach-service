import re

from django.db.models import F, DateField, IntegerField
from django.db.models.functions import Cast

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from attach.models import RegistrHistlpu
from attach.api.exceptions import InvalidParameters, InvalidDateFormatOrNone
from attach.api.serializers import GetPersonaDataSerializer


DATE_REGEX = r'\d{4}-\d\d-\d\d'

class GetNewAttachByPeriod(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if len(self.request.query_params) == 0:
            raise InvalidParameters
        
        query_begin_d = self.request.query_params.get('queryBeginD')
        query_end_d = self.request.query_params.get('queryEndD')
        if query_begin_d is None or query_end_d is None:
            raise InvalidParameters
        elif not re.fullmatch(DATE_REGEX, query_begin_d): 
            raise InvalidDateFormatOrNone('queryBeginD')
        elif not re.fullmatch(DATE_REGEX, query_end_d):
            raise InvalidDateFormatOrNone('queryEndD')
        else:
            attach_data = RegistrHistlpu.objects.using('registr').filter(
                lpudt__range=(query_begin_d, query_end_d))
        
        return attach_data
    
    def get(self, request, *args, **kwargs):
        new_attach = self.get_queryset()
        new_attach = new_attach.annotate(
            birth_day=Cast('pid__dr', output_field=DateField()),
            polis_beg=Cast('pid__dbeg', output_field=DateField()),
            polis_stop=Cast('pid__dstop', output_field=DateField()),
            lpudt_to_date=Cast('lpudt', output_field=DateField()),
            lpudx_to_date=Cast('lpudx', output_field=DateField()),
            lputype_to_int=Cast('lputype', output_field=IntegerField()),
            doctor_to_date=Cast('pid__lpudt_doc', output_field=DateField())
        ).values(
            'birth_day', 'polis_beg', 'polis_stop', 'lpu', 'oid', 'lpuauto',
            'district', 'ss_doctor', 'subdiv',
            enp=F('pid__enp'),
            ss=F('pid__ss'),
            fam=F('pid__fam'),
            im=F('pid__im'),
            ot=F('pid__ot'),
            q=F('pid__q'),
            attach_beg=F('lpudt_to_date'),
            attach_end=F('lpudx_to_date'),
            lpu_type=F('lputype_to_int'),
            doctor_since=F('doctor_to_date'),
        )
        serializer = GetPersonaDataSerializer(new_attach, many=True)

        context_list = []
        context_dict = {}

        for item in serializer.data:
            context_dict.clear()
            if 'externalRequestId' in self.request.query_params:
                context_dict['externalRequestId'] = self.request.query_params['externalRequestId']
            for k, v in item.items():
                if v is not None:
                    context_dict[k] = v
                    if k == 'doctorSnils' and len(v) == 11:
                        context_dict[k] = f'{context_dict[k][:3]}-{context_dict[k][3:6]}-{context_dict[k][6:9]} {context_dict[k][9:11]}'
            context_list.append(context_dict.copy())
        return Response(context_list, 200)