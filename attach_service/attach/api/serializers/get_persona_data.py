from rest_framework import serializers


class GetPersonaDataSerializer(serializers.Serializer):
    external_request_id = externalRequestId = serializers.CharField(required=False)
    enp = personaEnp = serializers.CharField()
    fam = personaFam = serializers.CharField()
    im = personaIm = serializers.CharField()
    ot = personaOt = serializers.CharField()
    birth_day = personaBirthday = serializers.DateField()
    ss = personaSnils = serializers.CharField()
    q = personaSmoCode = serializers.CharField()
    polis_beg = personaPolisBeginD = serializers.DateField()
    polis_stop = personaPolisEndD = serializers.DateField()
    lpu = moCode = serializers.CharField()
    oid = moOID = serializers.CharField()
    subdiv = moDepOID = serializers.CharField()
    attach_beg = attachBeginD = serializers.DateField()
    attach_end = attachEndD = serializers.DateField()
    lpuauto = attachMethod = serializers.IntegerField()
    lpu_type = attachType = serializers.IntegerField()
    district = areaOID = serializers.CharField()
    ss_doctor = doctorSnils = serializers.CharField()
    doctor_since = doctorSince = serializers.DateField()

