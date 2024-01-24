import re
from datetime import date, timedelta, datetime

from django.db.models import F, DateField, IntegerField, Q
from django.db.models.functions import Cast

from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer, OpenApiParameter

from attach.models import RegistrHistlpu
from attach.api.exceptions import InvalidParameters, InvalidDateFormatOrNone
from attach.api.serializers import GetAttachStatusChangeSerializer, GetPersonaDataSerializer


DATE_REGEX = r'\d{4}-\d\d-\d\d'

@extend_schema(
    tags=["Get attach and persona data"]
)
@extend_schema_view(
    get=extend_schema(
        summary="Получить информацию о прикрепленных гражданах за указанный период",
        request=GetAttachStatusChangeSerializer,
        responses={
            status.HTTP_200_OK : GetAttachStatusChangeSerializer,
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='ErrorCodeResponse',
                fields={
                    'code': serializers.CharField(),
                    'message': serializers.CharField(),
                }
            )
        },
        parameters=[
            OpenApiParameter(
                name='queryBeginD',
                location=OpenApiParameter.QUERY,
                description='Дата начала периода',
                required=True,
                type=date,
            ),
            OpenApiParameter(
                name='queryEndD',
                location=OpenApiParameter.QUERY,
                description='Дата окончания периода',
                required=True,
                type=date,
            ),
            OpenApiParameter(
                name='externalRequestId',
                location=OpenApiParameter.QUERY,
                description='Идентификатор запроса',
                required=False,
                type=str,
            ),
        ]
    )
)


class GetAttachStatusChangeView(APIView):
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
            query_end_d = (datetime.strptime(query_end_d, '%Y-%m-%d')  + timedelta(days=1)).strftime('%Y-%m-%d')
            attach_data = RegistrHistlpu.objects.using('registr').filter(
                Q(lpudt__range=(query_begin_d, query_end_d)) | Q(dedit__range=(query_begin_d, query_end_d))).filter(
                    lpudx__isnull=True
                )
            de_attach_data = RegistrHistlpu.objects.using('registr').filter(
                Q(lpudx__range=(query_begin_d, query_end_d)) | Q(dedit__range=(query_begin_d, query_end_d))).filter(
                    lpudx__isnull=False
                )
        
        return attach_data, de_attach_data
    
    def get(self, request, *args, **kwargs):
        new_attach, de_attach = self.get_queryset()
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

        de_attach = de_attach.annotate(
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

        attach_serializer = GetPersonaDataSerializer(new_attach, many=True)
        de_attach_serializer = GetPersonaDataSerializer(de_attach, many=True)

        context_list = {}
        attach_list = []
        context_dict = {}
        for item in attach_serializer.data:
            context_dict.clear()
            if 'externalRequestId' in self.request.query_params:
                context_dict['externalRequestId'] = self.request.query_params['externalRequestId']
            for k, v in item.items():
                if k == 'attachType' and v is None:
                    context_dict[k] = 99
                if v is not None:
                    context_dict[k] = v
                    if k == 'doctorSnils' and len(v) == 11:
                        context_dict[k] = f'{context_dict[k][:3]}-{context_dict[k][3:6]}-{context_dict[k][6:9]} {context_dict[k][9:11]}'
            attach_list.append(context_dict.copy())

        context_list['attachList'] = attach_list.copy()
        attach_list.clear()

        for item in de_attach_serializer.data:
            context_dict.clear()
            if 'externalRequestId' in self.request.query_params:
                context_dict['externalRequestId'] = self.request.query_params['externalRequestId']
            for k, v in item.items():
                if k == 'attachType' and v is None:
                    context_dict[k] = 99
                if v is not None:
                    context_dict[k] = v
                    if k == 'doctorSnils' and len(v) == 11:
                        context_dict[k] = f'{context_dict[k][:3]}-{context_dict[k][3:6]}-{context_dict[k][6:9]} {context_dict[k][9:11]}'
            attach_list.append(context_dict.copy())

        context_list['deAttachList'] = attach_list.copy()
        return Response(context_list, 200)