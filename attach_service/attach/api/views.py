import datetime
from secrets import token_hex

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from attach.api.serializers import HislpuSerializer, GetViewDataAttachStartSerializer, GetViewDataAttachPollSerializer
from attach.models import Histlpu, GetViewDataAttachStart, GetViewDataAttachPoll


#class HistlpuViewSet(viewsets.ReadOnlyModelViewSet):
#    queryset = Histlpu.objects.filter(dedit__gte=datetime.date(2023, 11, 21)).filter(lpu='530002')
#    serializer_class = HislpuSerializer


class GetViewDataAttachStartView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = GetViewDataAttachStartSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            op_token = token_hex(16)
            data_attach = GetViewDataAttachStart(
                external_request_id=serializer.data['external_request_id'],
                op_token=op_token,
                date_query=serializer.data['date_query']
            )
            data_attach.save()

            attach_poll = GetViewDataAttachPoll(
                op_token=op_token,
                status='PROCESS' 
            )
            attach_poll.save()

            response_context = {
                "externalRequestId": serializer.data['external_request_id'],
                "opToken": op_token,
            }
            return Response(response_context, 200)
        

class GetViewDataAttachPollView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = GetViewDataAttachPollSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            poll_file = GetViewDataAttachPoll.objects.get(op_token=serializer.data['op_token'])
            poll_file.external_request_id = serializer.data['external_request_id']
            poll_file.save()

            response_context = {
                "externalRequestId": serializer.data['external_request_id'],
                "status": poll_file.status,
            }
            if poll_file.status == 'COMPLITE':
                response_context["viewAttachFile"] = poll_file.poll_file
            return Response(response_context, 200)