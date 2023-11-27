import datetime
from secrets import token_hex

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from attach.api.serializers import HislpuSerializer, GetViewDataAttachStartSerializer
from attach.models import Histlpu, GetViewDataAttachStart


#class HistlpuViewSet(viewsets.ReadOnlyModelViewSet):
#    queryset = Histlpu.objects.filter(dedit__gte=datetime.date(2023, 11, 21)).filter(lpu='530002')
#    serializer_class = HislpuSerializer


class GetViewDataAttachStartView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = GetViewDataAttachStartSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            op_token = token_hex(16)
            op_data = GetViewDataAttachStart(
                external_request_id=serializer.data['external_request_id'],
                op_token=op_token,
                date_query=serializer.data['date_query']
            )
            op_data.save()
            return Response(op_token, 200)