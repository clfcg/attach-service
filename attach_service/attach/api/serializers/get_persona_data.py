from rest_framework import serializers


class GetPersonaDataSerializer(serializers.Serializer):
    external_request_id = externalRequestId = serializers.CharField(required=False)
    enp = personaEnp = serializers.CharField(required=False)
    fam = personaFam = serializers.CharField(required=False)
    im = personaIm = serializers.CharField(required=False)
    ot = personaOt = serializers.CharField(required=False)
    birth_day = personaBirthday = serializers.DateField(required=False)
    ss = personaSnils = serializers.CharField(required=False)
    q = personaSmoCode = serializers.CharField(required=False)
    polis_beg = personaPolisBeginD = serializers.DateField(required=False)
    polis_stop = personaPolisEndD = serializers.DateField(required=False)
    lpu = moCode = serializers.CharField(required=False)
    oid = moOID = serializers.CharField(required=False)
    subdiv = moDepOID = serializers.CharField(required=False)
    attach_beg = attachBeginD = serializers.DateField(required=False)
    attach_end = attachEndD = serializers.DateField(required=False)
    lpuauto = attachMethod = serializers.IntegerField(required=False)
    lpu_type = attachType = serializers.IntegerField(required=False)
    district = areaOID = serializers.CharField(required=False)
    ss_doctor = doctorSnils = serializers.CharField(required=False)
    doctor_since = doctorSince = serializers.DateField(required=False)

