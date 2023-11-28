from rest_framework import serializers

from attach.models import Histlpu, People, GetViewDataAttachPoll
from .exceptions import InvalidAttachFieldException


class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = ['enp', 'ss', 'fam', 'im', 'ot']


class HislpuSerializer(serializers.Serializer):
    pid = persona = PeopleSerializer(read_only=True)

    #pid = serializers.IntegerField() # ЕНП
    lpudt = serializers.DateTimeField()
    lpudx = serializers.DateTimeField()
    lpuauto = serializers.IntegerField()
    lputype = serializers.IntegerField()
    district = serializers.CharField(max_length=64)
    oid = serializers.CharField(max_length=64)
    # moFId
    # doctorId
    lpu = serializers.CharField(max_length=6)
    ss_doctor = serializers.CharField(max_length=11)
    # doctorSince
    subdiv = serializers.CharField(max_length=64)
    dedit = serializers.DateTimeField()


class GetViewDataAttachStartSerializer(serializers.Serializer):
    def validate(self, data):
        if 'external_request_id' not in data.keys():
            print(data.keys())
            raise InvalidAttachFieldException('Значение параметра externalRequestId должно быть заполнено.')
        if 'date_query' not in data.keys():
            raise InvalidAttachFieldException('Значение параметра dateQuery должно быть заполнено.')
        return data

    external_request_id = serializers.CharField(max_length=50, required=False)
    date_query = serializers.DateField(required=False)


class GetViewDataAttachPollSerializer(serializers.Serializer):
    def validate(self, data):
        if 'external_request_id' not in data.keys() and data['external_request_id'] == '':
            raise InvalidAttachFieldException('idRequest is needed')
        if len(GetViewDataAttachPoll.objects.filter(op_token__in=data['op_token'])) == 0 and data['op_token'] == '':
            raise InvalidAttachFieldException('opToken is needed')
        return data

    external_request_id = serializers.CharField(max_length=50, required=False)
    op_token = serializers.CharField(max_length=50, required=False)