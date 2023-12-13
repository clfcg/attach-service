from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from attach.api.serializers import RegisterAttachSerializer
from attach.api.exceptions import MoreThanOnePerson, PersonNotFound, NotActivePolis
from attach.models.attach_test import RegisterAttach, RegistrPeople


class RegisterAttachView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = RegisterAttachSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            pers = RegistrPeople.objects.using('registr').filter(enp=serializer.data['enp'])
            if len(pers) > 1:
                raise MoreThanOnePerson()
            elif len(pers) == 0:
                raise PersonNotFound()
            else:
                pers = pers.filter(
                    dbeg__lt=serializer.data['dateAttachB']).filter(
                        Q(dstop__isnull=True) | Q(dstop__gt=serializer.data['dateAttachB']))
                if len(pers) == 0:
                    raise NotActivePolis()
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
                    user=Token.objects.get(request.headers['Authorization'][6:])
                )
                attach_send.save()
            print(serializer.data,request.headers)
            return Response(serializer.data, 200)