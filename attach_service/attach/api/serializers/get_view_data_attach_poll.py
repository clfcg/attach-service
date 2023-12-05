from rest_framework import serializers

from attach.models import GetViewDataAttachPoll
from attach.api.exceptions import ParameterIsRequired, ParameterDataIsRequired, InvalidOpToken


class GetViewDataAttachPollSerializer(serializers.Serializer):
    externalRequestId = serializers.CharField(max_length=50, required=False, allow_blank=True)
    opToken = serializers.CharField(max_length=50, required=False, allow_blank=True)

    def validate(self, data):
        if 'externalRequestId' not in data.keys():
            raise ParameterIsRequired('externalRequestId')
        if data['externalRequestId'] == '':
            raise ParameterDataIsRequired('externalRequestId')
        if 'opToken' not in data.keys():
            raise ParameterIsRequired('opToken')
        if data['opToken'] == '':
            raise ParameterDataIsRequired('opToken')
        if len(GetViewDataAttachPoll.objects.filter(op_token__in=[data['opToken']])) == 0:
            raise InvalidOpToken(data['opToken'])
        return data