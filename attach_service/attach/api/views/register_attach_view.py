from datetime import datetime, timedelta, date
import uuid

from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from attach.api.serializers import RegisterAttachSerializer
from attach.api.exceptions import MoreThanOnePerson, PersonNotFound, NotActivePolis, MPIError
from attach.models import RegisterAttach, RegistrPeople, StatusAttach, RegistrHistlpu
from attach.api.utils.mpi_register_attach import MpiRegisterAttachMixin


class RegisterAttachView(MpiRegisterAttachMixin, APIView):
    mixin_template_soap = "mpi_register_attach.xml"
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

            pers = RegistrPeople.objects.using('registr').filter(enp=serializer.data['enp']).filter(
                Q(dstop__isnull=True) | Q(dstop__gt=serializer.data['dateAttachB'])
            )
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
                RegisterAttach.objects.filter(pk=attach_send.pk).update(pid=pers[0].pk)
                polis = pers[0].polis.filter(
                    dbeg__lte=serializer.data['dateAttachB']).filter(
                        Q(dstop__isnull=True) | Q(dstop__gt=serializer.data['dateAttachB'])
                    )
                if len(polis) == 0:
                    RegisterAttach.objects.filter(pk=attach_send.pk).update(
                        rs_err=NotActivePolis().default_code,
                        remark_err=NotActivePolis().detail,
                        status=StatusAttach.objects.get(status_code=2)
                    )
                    raise NotActivePolis()
                
                attach = pers[0].attach.filter(lpudx__isnull=True)

                attach_update = pers[0].attach.filter(
                    lpu=serializer.data['moCode'],
                    lputype=str(serializer.data['areaType']),
                    lpudx__isnull=True,
                )
                attach_areatype = pers[0].attach.filter(
                    lpu=serializer.data['moCode'],
                    lpudx__isnull=True,
                    lputype__isnull=False,
                ).exclude(lputype=str(serializer.data['areaType']))

                attach_before = pers[0].attach.filter(
                    lpudx__isnull=True,
                ).filter(
                    Q(lputype__isnull=True) | Q(lputype='')
                )
                attach_current = pers[0].attach.filter(
                    lputype=str(serializer.data['areaType']),
                    lpudx__isnull=True,
                ).exclude(lpu=serializer.data['moCode'])

                ss_doctor_format = "".join(c for c in serializer.data['snilsDoctor'] if c.isdecimal())

                # Запрос в ФЕРЗЛ
                self.mixin_cleaned_data = serializer.data
                self.mixin_cleaned_data['rguid'] = uuid.uuid4()
                self.pid = pers[0].pk
                self.attach_id = RegisterAttach.objects.get(pk=attach_send.pk)
                self.mixin_cleaned_data['snilsDoctor'] = ss_doctor_format
                response_data = self.mixin_mpi_response()
                if 'err_code' in response_data.keys():
                    RegisterAttach.objects.filter(pk=attach_send.pk).update(
                        ferzl_err=response_data['err_code'],
                        remark_err=response_data['err_message'],
                        status=StatusAttach.objects.get(status_code=3)
                    )
                    raise MPIError(response_data['err_code'], response_data['err_message'])

                # Нашлось прикрепление по коду МО и типу участка
                if len(attach_update) != 0:
                    for attach_item in attach_update:
                        RegistrHistlpu.objects.using('registr').filter(pk=attach_item.pk).update(
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
                    if str(serializer.data['areaType']) == '1':
                        RegistrPeople.objects.using('registr').filter(pk=pers[0].pk).update(
                            lpu=serializer.data['moCode'],
                            lpuauto=serializer.data['attachMethod'],
                            lputype=serializer.data['areaType'],
                            lpudt=serializer.data['dateAttachB'],
                            lpudx=serializer.data['dateAttachE'],
                            ss_doctor=ss_doctor_format,
                            lpudt_doc=serializer.data['doctorSince'],
                        )                       
                    RegisterAttach.objects.filter(pk=attach_send.pk).update(
                        status=StatusAttach.objects.get(status_code=1)
                    )

                elif len(attach_current) != 0:
                    for attach_item in attach_current:
                        RegistrHistlpu.objects.using('registr').filter(pk=attach_item.pk).update(
                            dedit=datetime.now(),
                            lpudx=datetime.strptime(serializer.data['dateAttachB'], '%Y-%m-%d').date()-timedelta(days=1),
                        )
                    new_attach = RegistrHistlpu(
                        pid=RegistrPeople.objects.using('registr').get(pk=pers[0].pk),
                        dedit=datetime.now(),
                        lpudt=serializer.data['dateAttachB'],
                        lpudx=serializer.data['dateAttachE'],
                        lpuauto=serializer.data['attachMethod'],
                        lputype=serializer.data['areaType'],
                        district=serializer.data['areaId'],
                        oid=serializer.data['moId'],
                        lpu=serializer.data['moCode'],
                        subdiv=serializer.data['moDepId'],
                        ss_doctor=ss_doctor_format,
                    )
                    new_attach.save()
                    if str(serializer.data['areaType']) == '1':
                        RegistrPeople.objects.using('registr').filter(pk=pers[0].pk).update(
                            lpu=serializer.data['moCode'],
                            lpuauto=serializer.data['attachMethod'],
                            lputype=serializer.data['areaType'],
                            lpudt=serializer.data['dateAttachB'],
                            lpudx=serializer.data['dateAttachE'],
                            ss_doctor=ss_doctor_format,
                            lpudt_doc=serializer.data['doctorSince'],
                        )                       
                    RegisterAttach.objects.filter(pk=attach_send.pk).update(
                        status=StatusAttach.objects.get(status_code=1)
                    )

                elif len(attach_before) != 0:
                    if str(serializer.data['areaType']) == '1':
                        for attach_item in attach_before:
                            RegistrHistlpu.objects.using('registr').filter(pk=attach_item.pk).update(
                                dedit=datetime.now(),
                                lpudx=datetime.strptime(serializer.data['dateAttachB'], '%Y-%m-%d').date()-timedelta(days=1),
                            )

                        new_attach = RegistrHistlpu(
                            pid=RegistrPeople.objects.using('registr').get(pk=pers[0].pk),
                            dedit=datetime.now(),
                            lpudt=serializer.data['dateAttachB'],
                            lpudx=serializer.data['dateAttachE'],
                            lpuauto=serializer.data['attachMethod'],
                            lputype=serializer.data['areaType'],
                            district=serializer.data['areaId'],
                            oid=serializer.data['moId'],
                            lpu=serializer.data['moCode'],
                            subdiv=serializer.data['moDepId'],
                            ss_doctor=ss_doctor_format,
                        )
                        new_attach.save()
                        RegistrPeople.objects.using('registr').filter(pk=pers[0].pk).update(
                            lpu=serializer.data['moCode'],
                            lpuauto=serializer.data['attachMethod'],
                            lputype=serializer.data['areaType'],
                            lpudt=serializer.data['dateAttachB'],
                            lpudx=serializer.data['dateAttachE'],
                            ss_doctor=ss_doctor_format,
                            lpudt_doc=serializer.data['doctorSince'],
                        )
                        RegisterAttach.objects.filter(pk=attach_send.pk).update(
                            status=StatusAttach.objects.get(status_code=1)
                        )

                    else:
                        new_attach = RegistrHistlpu(
                            pid=RegistrPeople.objects.using('registr').get(pk=pers[0].pk),
                            dedit=datetime.now(),
                            lpudt=serializer.data['dateAttachB'],
                            lpudx=serializer.data['dateAttachE'],
                            lpuauto=serializer.data['attachMethod'],
                            lputype=serializer.data['areaType'],
                            district=serializer.data['areaId'],
                            oid=serializer.data['moId'],
                            lpu=serializer.data['moCode'],
                            subdiv=serializer.data['moDepId'],
                            ss_doctor=ss_doctor_format,
                        )
                        new_attach.save()
                        RegisterAttach.objects.filter(pk=attach_send.pk).update(
                            status=StatusAttach.objects.get(status_code=1)
                        )

                elif len(attach_areatype) != 0:
                    new_attach = RegistrHistlpu(
                        pid=RegistrPeople.objects.using('registr').get(pk=pers[0].pk),
                        dedit=datetime.now(),
                        lpudt=serializer.data['dateAttachB'],
                        lpudx=serializer.data['dateAttachE'],
                        lpuauto=serializer.data['attachMethod'],
                        lputype=serializer.data['areaType'],
                        district=serializer.data['areaId'],
                        oid=serializer.data['moId'],
                        lpu=serializer.data['moCode'],
                        subdiv=serializer.data['moDepId'],
                        ss_doctor=ss_doctor_format,
                    )
                    new_attach.save()
                    if str(serializer.data['areaType']) == '1':
                        RegistrPeople.objects.using('registr').filter(pk=pers[0].pk).update(
                            lpu=serializer.data['moCode'],
                            lpuauto=serializer.data['attachMethod'],
                            lputype=serializer.data['areaType'],
                            lpudt=serializer.data['dateAttachB'],
                            lpudx=serializer.data['dateAttachE'],
                            ss_doctor=ss_doctor_format,
                            lpudt_doc=serializer.data['doctorSince'],
                        )                       
                    RegisterAttach.objects.filter(pk=attach_send.pk).update(
                        status=StatusAttach.objects.get(status_code=1)
                    )

                else:
                    if len(attach) != 0:
                        for attach_item in attach:
                            if attach_item.lputype is None or attach_item.lputype == '':
                                RegistrHistlpu.objects.using('registr').filter(pk=attach_item.pk).update(
                                    dedit=datetime.now(),
                                    lpudx=datetime.strptime(serializer.data['dateAttachB'], '%Y-%m-%d').date()-timedelta(days=1),
                                )
                        new_attach = RegistrHistlpu(
                            pid=RegistrPeople.objects.using('registr').get(pk=pers[0].pk),
                            dedit=datetime.now(),
                            lpudt=serializer.data['dateAttachB'],
                            lpudx=serializer.data['dateAttachE'],
                            lpuauto=serializer.data['attachMethod'],
                            lputype=serializer.data['areaType'],
                            district=serializer.data['areaId'],
                            oid=serializer.data['moId'],
                            lpu=serializer.data['moCode'],
                            subdiv=serializer.data['moDepId'],
                            ss_doctor=ss_doctor_format,
                        )
                        new_attach.save()
                        if str(serializer.data['areaType']) == '1':
                            RegistrPeople.objects.using('registr').filter(pk=pers[0].pk).update(
                                lpu=serializer.data['moCode'],
                                lpuauto=serializer.data['attachMethod'],
                                lputype=serializer.data['areaType'],
                                lpudt=serializer.data['dateAttachB'],
                                lpudx=serializer.data['dateAttachE'],
                                ss_doctor=ss_doctor_format,
                                lpudt_doc=serializer.data['doctorSince'],
                            )                       
                        RegisterAttach.objects.filter(pk=attach_send.pk).update(
                            status=StatusAttach.objects.get(status_code=1)
                        )
                    else:
                        new_attach = RegistrHistlpu(
                            pid=RegistrPeople.objects.using('registr').get(pk=pers[0].pk),
                            dedit=datetime.now(),
                            lpudt=serializer.data['dateAttachB'],
                            lpudx=serializer.data['dateAttachE'],
                            lpuauto=serializer.data['attachMethod'],
                            lputype=serializer.data['areaType'],
                            district=serializer.data['areaId'],
                            oid=serializer.data['moId'],
                            lpu=serializer.data['moCode'],
                            subdiv=serializer.data['moDepId'],
                            ss_doctor=ss_doctor_format,
                        )
                        new_attach.save()
                        if str(serializer.data['areaType']) == '1':
                            RegistrPeople.objects.using('registr').filter(pk=pers[0].pk).update(
                                lpu=serializer.data['moCode'],
                                lpuauto=serializer.data['attachMethod'],
                                lputype=serializer.data['areaType'],
                                lpudt=serializer.data['dateAttachB'],
                                lpudx=serializer.data['dateAttachE'],
                                ss_doctor=ss_doctor_format,
                                lpudt_doc=serializer.data['doctorSince'],
                            )                       
                        RegisterAttach.objects.filter(pk=attach_send.pk).update(
                            status=StatusAttach.objects.get(status_code=1)
                        )

            context = {}
            for k, v in serializer.data.items():
                if v is not None:
                    context[k] = v

            return Response(context, 200)