from datetime import date

from django.db.models import Q, F, DateField, IntegerField
from django.db.models.functions import Cast

from rest_framework.views import APIView
from rest_framework.response import Response

from attach.models import RegistrPeople
from attach.api.exceptions import InvalidParameters, PersonNotFound, MoreThanOnePerson
from attach.api.serializers import GetPersonaDataSerializer


class GetPersonaDataView(APIView):
    def get_queryset(self):
        # Проверка наличия параметров в запросе
        if len(self.request.query_params) == 0:
            raise InvalidParameters()
        
        # Параметры запроса
        pers = RegistrPeople.objects.using('registr').filter(Q(dstop__isnull=True) | Q(dstop__gt=date.today()))
        enp = self.request.query_params.get('enp')
        ss = self.request.query_params.get('ss')
        fam = self.request.query_params.get('fam')
        im = self.request.query_params.get('im')
        ot = self.request.query_params.get('ot')
        dr = self.request.query_params.get('dr')
        if enp is not None:
            pers = pers.filter(enp=enp)
        elif ss is not None:
            pers = pers.filter(ss=ss)
        elif fam is not None and im is not None and ot is not None and dr is not None:
            pers = pers.filter(fam=fam, im=im, ot=ot, dr=dr)
        elif fam is not None and im is not None and dr is not None:
            pers = pers.filter(fam=fam, im=im, dr=dr)
        else:
            raise InvalidParameters()
        
        # Проверка результата запроса
        if len(pers) == 0:
            raise PersonNotFound()
        elif len(pers) > 1:
            raise MoreThanOnePerson()
        else:
            for item in pers:
                person_attach = item.attach.filter(lpudx__isnull=True)
        
        if len(person_attach) == 0:
            return pers
        else:
            return person_attach
    
    def get(self, request, *args, **kwargs):
        person_attach = self.get_queryset()
        if person_attach.model.__name__ == 'RegistrPeople':
            person_attach = person_attach.annotate(
                dr_to_date=Cast('dr', output_field=DateField()),
                dbeg_to_date=Cast('dbeg', output_field=DateField()),
                dstop_to_date=Cast('dstop', output_field=DateField()),
            ).annotate(
                birth_day=F('dr_to_date'),
                polis_beg=F('dbeg_to_date'),
                polis_stop=F('dstop_to_date'),
            )

        if person_attach.model.__name__ == 'RegistrHistlpu':
            person_attach = person_attach.annotate(
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

        serializer = GetPersonaDataSerializer(person_attach[0])
        context = {}
        if 'externalRequestId' in self.request.query_params:
            context['externalRequestId'] = self.request.query_params['externalRequestId']
        for k, v in serializer.data.items():
            if v is not None:
                context[k] = v
                if k == 'doctorSnils' and len(v) == 11:
                    context[k] = f'{context[k][:3]}-{context[k][3:6]}-{context[k][6:9]} {context[k][9:11]}'
        return Response(context, 200)