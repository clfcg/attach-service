from rest_framework import serializers
from attach.models import Histlpu, People


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



#class HislpuSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Histlpu
#        fields = ['pid', 'lpu', 'lpuauto', 'lpudt', 'lpudx', ]