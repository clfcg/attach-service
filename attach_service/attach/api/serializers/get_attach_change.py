from rest_framework import serializers

from .get_persona_data import GetPersonaDataSerializer


class GetAttachStatusChangeSerializer(serializers.Serializer):
    attachList = GetPersonaDataSerializer(many=True)
    deAttachList = GetPersonaDataSerializer(many=True)