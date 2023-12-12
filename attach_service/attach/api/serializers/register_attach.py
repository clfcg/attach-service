from rest_framework import serializers


class registerAttachSerializer(serializers.Serializer):
    external_request_id = externalRequestId = serializers.CharField()
    enp = serializers.CharField()
    date_attach_b = dateAttachB = serializers.DateField()
    date_attach_e = dateAttachE = serializers.DateField()
    attach_method = attachMethod = serializers.IntegerField()
    area_type = areaType = serializers.IntegerField()
    area_id = areaId = serializers.CharField()
    mo_id = moId = serializers.CharField()
    mo_code = moCode = serializers.CharField()
    mo_f_id = moFId = serializers.CharField()
    doctor_id = doctorId = serializers.CharField()
    snils_doctor = snilsDoctor = serializers.CharField()
    doctor_since = doctorSince = serializers.DateField()
    mo_dep_id = moDepId = serializers.CharField()

