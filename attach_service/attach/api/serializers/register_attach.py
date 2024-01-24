import re

from rest_framework import serializers
import attach.api.exceptions as ex


DATE_REGEX = r'\d{4}-\d\d-\d\d'
ENP_REGEX = r'\d{16}'

class RegisterAttachSerializer(serializers.Serializer):
    externalRequestId = serializers.CharField(required=False, allow_blank=True)
    enp = serializers.CharField(required=False, allow_blank=True)
    dateAttachB = serializers.DateField(required=False, allow_null=True)
    dateAttachE = serializers.DateField(required=False, allow_null=True)
    attachMethod = serializers.IntegerField(required=False)
    areaType = serializers.IntegerField(required=False)
    areaId = serializers.CharField(required=False, allow_blank=True, default=None)
    moId = serializers.CharField(required=False, allow_blank=True)
    moCode = serializers.CharField(required=False, allow_blank=True)
    moFId = serializers.CharField(required=False, allow_blank=True, default=None)
    doctorId = serializers.CharField(required=False, allow_blank=True, default=None)
    snilsDoctor = serializers.CharField(required=False, allow_blank=True, default=None)
    doctorSince = serializers.DateField(required=False, allow_null=True)
    moDepId = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        req_list = ['externalRequestId', 'enp', 'dateAttachB', 'attachMethod',
                    'areaType', 'moId', 'moCode', 'moDepId']

        for field in req_list:
            if field not in data.keys():
                raise ex.ParameterIsRequired(field)
            if data[field] == '': 
                raise ex.ParameterDataIsRequired(field)
            if data[field] is None :
                raise ex.InvalidDateFormatOrNone(field)
        
        if data['attachMethod'] not in [1, 2, 3]:
            raise ex.InvalidAttachMethod()
        if data['areaType'] not in [1, 2, 3]:
            raise ex.InvalidAreaType()
        
        if not re.fullmatch(ENP_REGEX, data['enp']):
            raise ex.InvalidEnpLen()
        if 'dateAttachE' in data.keys() and data['dateAttachE'] is None:
            raise ex.InvalidDateFormatOrNone('dateAttachE')
        if 'doctorSince' in data.keys() and data['doctorSince'] is None:
            raise ex.InvalidDateFormatOrNone('doctorSince')
        return data
    
    def to_internal_value(self, data):
        date_list = ['dateAttachB', 'dateAttachE', 'doctorSince']
        for field in date_list:
            if field in data.keys():
                if data[field] == '' or not re.fullmatch(DATE_REGEX, data[field]):
                    data[field] = None
        
        int_list = ['attachMethod', 'areaType']
        for field in int_list:
            if field in data.keys():
                try:
                    data[field] = int(data[field])
                except:
                    data[field] = 999
        return super(RegisterAttachSerializer, self).to_internal_value(data)