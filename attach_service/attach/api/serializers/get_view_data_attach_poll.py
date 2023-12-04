from rest_framework import serializers

from attach.api.exceptions import InvalidAttachFieldException
from attach.models import GetViewDataAttachPoll


class GetViewDataAttachPollSerializer(serializers.Serializer):
    def validate(self, data):
        if 'external_request_id' not in data.keys() and data['external_request_id'] == '':
            raise InvalidAttachFieldException('idRequest is needed')
        if len(GetViewDataAttachPoll.objects.filter(op_token__in=data['op_token'])) == 0 and data['op_token'] == '':
            raise InvalidAttachFieldException('opToken is needed')
        return data

    external_request_id = serializers.CharField(max_length=50, required=False)
    op_token = serializers.CharField(max_length=50, required=False)