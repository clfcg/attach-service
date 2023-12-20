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
                ss_doctor_format = "".join(c for c in serializer.data['snilsDoctor'] if c.isdecimal())
                if len(attach) == 1:
                    for attach_item in attach:
                        if (attach_item.lpu == serializer.data['moCode'] and 
                            (attach_item.lputype == str(serializer.data['areaType']) or attach_item.lputype is None)):

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
                            RegistrPeople.objects.using('registr').filter(pk=pers[0].pk).update(
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
                        
                        if (attach_item.lpu == serializer.data['moCode'] and 
                            attach_item.lputype != str(serializer.data['areaType']) and 
                            attach_item.lputype is not None):
                            
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

                        if (attach_item.lpu != serializer.data['moCode']):

                            #Запрос в ФЕРЗЛ
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
                    
                elif len(attach) > 1:
                    check_list = set()
                    for attach_item in attach:
                        check_list.add((attach_item.lpu, attach_item.lputype))
                    print(check_list)
                    if len(check_list) == 1:
                        #Запрос в ФЕРЗЛ
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

                        for attach_item in attach:
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
                        
                    if len(check_list) > 1 and check_list[0][0] != check_list[1][0]:
                        #Запрос в ФЕРЗЛ
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
                        
                        for attach_item in attach:
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
                        
                    if len(check_list) > 1 and check_list[0][0] == check_list[1][0] and check_list[0][0] == serializer.data['moCode']:
                        #Запрос в ФЕРЗЛ
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
                        
                        for attach_item in attach:
                            if attach_item.lputype == str(serializer.data['areaType']):
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
                                
                    if len(check_list) > 1 and check_list[0][0] == check_list[1][0] and check_list[0][0] != serializer.data['moCode']:
                        #Запрос в ФЕРЗЛ
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
                        
                        for attach_item in attach:
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
                    #Запрос в ФЕРЗЛ
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
                    
                    context = {}
                    for k, v in serializer.data.items():
                        if v is not None:
                            context[k] = v

            return Response(context, 200)