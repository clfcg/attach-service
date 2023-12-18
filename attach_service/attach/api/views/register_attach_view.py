from datetime import datetime

from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from attach.api.serializers import RegisterAttachSerializer
from attach.api.exceptions import MoreThanOnePerson, PersonNotFound, NotActivePolis
from attach.models import RegisterAttach, RegistrPeople, StatusAttach, RegistrHistlpu


class RegisterAttachView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = RegisterAttachSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Записать переданные данные по прикреплению в таблицу RegisterAttach
            attach_send = RegisterAttach(
                    external_request_id=serializer.data['externalRequestId'],
                    enp=serializer.data['enp'],
                    date_attach_b=serializer.data['dateAttachB'],
                    date_attach_e=serializer.data['dateAttachE'],
                    attach_method=serializer.data['attachMethod'],
                    area_type=serializer.data['areaType'],
                    area_id=serializer.data['areaId'],
                    mo_id=serializer.data['moId'],
                    mo_code=serializer.data['moCode'],
                    mo_f_id=serializer.data['moFId'],
                    doctor_id=serializer.data['doctorId'],
                    snils_doctor=serializer.data['snilsDoctor'],
                    doctor_since=serializer.data['doctorSince'],
                    mo_dep_id=serializer.data['moDepId'],
                    status=StatusAttach.objects.get(status_code=4),
                    user=Token.objects.get(key=request.headers['Authorization'][6:]).user
                )
            attach_send.save()

            pers = RegistrPeople.objects.using('registr').filter(enp=serializer.data['enp'])
            if len(pers) > 1:
                RegisterAttach.objects.filter(pk=attach_send.pk).update(
                    rs_err=MoreThanOnePerson().default_code,
                    remark_err=MoreThanOnePerson().detail,
                    status=StatusAttach.objects.get(status_code=2)
                )
                raise MoreThanOnePerson()
            elif len(pers) == 0:
                RegisterAttach.objects.filter(pk=attach_send.pk).update(
                    rs_err=PersonNotFound().default_code,
                    remark_err=PersonNotFound().detail,
                    status=StatusAttach.objects.get(status_code=2)
                )
                raise PersonNotFound()
            else:
                polis = pers[0].polis.filter(
                    dbeg__lte=serializer.data['dateAttachB']).filter(
                        Q(dstop__isnull=True) | Q(dstop__gt=serializer.data['dateAttachB'])
                    )
                # pers = pers.filter(
                #     dbeg__lte=serializer.data['dateAttachB']).filter(
                #         Q(dstop__isnull=True) | Q(dstop__gt=serializer.data['dateAttachB'])
                #     )
                if len(polis) == 0:
                    RegisterAttach.objects.filter(pk=attach_send.pk).update(
                        rs_err=NotActivePolis().default_code,
                        remark_err=NotActivePolis().detail,
                        status=StatusAttach.objects.get(status_code=2)
                    )
                    raise NotActivePolis()
                attach = pers[0].attach.filter(
                    Q(lpudx__isnull=True) | Q(lpudx__gt=serializer.data['dateAttachB'])
                )
                ss_doctor_format = "".join(c for c in serializer.data['snilsDoctor'] if c.isdecimal())
                if len(attach) == 1:
                    if (attach[0].lpu == serializer.data['moCode'] and 
                        (attach[0].lputype == serializer.data['areaType'] or attach[0].lputype is None)):
                        RegistrHistlpu.objects.using('registr').filter(pk=attach[0].pk).update(
                            dedit=datetime.now(),
                            lpudt=serializer.data['dateAttachB'],
                            lpudx=serializer.data['dateAttachE'],
                            lpuauto=serializer.data['attachMethod'],
                            lputype=serializer.data['areaType'],
                            district=serializer.data['areaId'],
                            oid=serializer.data['moId'],
                            subdiv=serializer.data['moDepId'],
                            ss_doctor=ss_doctor_format,
                        )
                        RegistrPeople.objects.using('registr').filter(pk=pers[0].pk).update(
                            lpuauto=serializer.data['attachMethod'],
                            lputype=serializer.data['areaType'],
                            lpudt=serializer.data['dateAttachB'],
                            lpudx=serializer.data['dateAttachE'],
                            ss_doctor=ss_doctor_format,
                            lpudt_doc=serializer.data['doctorSince'],
                        )
                        print(attach[0].pk, pers[0].pk)

            return Response(serializer.data, 200)