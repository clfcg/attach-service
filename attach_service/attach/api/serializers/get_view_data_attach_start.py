from rest_framework import serializers

from attach.api.exceptions import InvalidAttachFieldException


class GetViewDataAttachStartSerializer(serializers.Serializer):
    external_request_id = serializers.CharField(max_length=50, required=False)
    date_query = serializers.DateField(required=False)

    def validate(self, data):
        if 'external_request_id' not in data.keys():
            print(data.keys())
            raise InvalidAttachFieldException('Значение параметра externalRequestId должно быть заполнено.')
        if 'date_query' not in data.keys():
            raise InvalidAttachFieldException('Значение параметра dateQuery должно быть заполнено.')
        return data

    external_request_id = serializers.CharField(max_length=50, required=False)
    date_query = serializers.DateField(required=False)