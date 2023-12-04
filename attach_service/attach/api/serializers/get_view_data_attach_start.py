import re

from rest_framework import serializers

from attach.api.exceptions import ParameterIsRequired, ParameterDataIsRequired, InvalidDateFormatOrNone


DATE_REGEX = r'\d{4}-\d\d-\d\d'

class GetViewDataAttachStartSerializer(serializers.Serializer):
    externalRequestId = serializers.CharField(max_length=64, required=False, allow_blank=True)
    dateQuery = serializers.DateField(required=False, allow_null=True)

    def validate(self, data):
        if 'externalRequestId' not in data.keys():
            raise ParameterIsRequired('externalRequestId')
        if data['externalRequestId'] == '':
            raise ParameterDataIsRequired('externalRequestId')
        if 'dateQuery' not in data.keys():
            raise ParameterIsRequired('dateQuery')
        if data['dateQuery'] is None:
            raise InvalidDateFormatOrNone('dateQuery')
        return data
    
    def to_internal_value(self, data):
        if 'dateQuery' in data.keys():
            if data['dateQuery'] == '' or not re.fullmatch(DATE_REGEX, data['dateQuery']):
                data['dateQuery'] = None
        return super(GetViewDataAttachStartSerializer, self).to_internal_value(data)