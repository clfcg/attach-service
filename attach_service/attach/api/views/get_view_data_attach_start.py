from secrets import token_hex

from rest_framework.views import APIView
from rest_framework.response import Response

from attach.api.serializers import GetViewDataAttachStartSerializer
from attach.models import GetViewDataAttachStart, GetViewDataAttachPoll
from attach.tasks import generate_attach_file


class GetViewDataAttachStartView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = GetViewDataAttachStartSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            op_token = token_hex(16)
            data_attach = GetViewDataAttachStart(
                external_request_id=serializer.data['externalRequestId'],
                op_token=op_token,
                date_query=serializer.data['dateQuery']
            )
            data_attach.save()

            attach_poll = GetViewDataAttachPoll(
                op_token=op_token,
                status='PROCESS' 
            )
            attach_poll.save()

            generate_attach_file.send(op_token, serializer.data['dateQuery'])
            response_context = {
                "externalRequestId": serializer.data['externalRequestId'],
                "opToken": op_token,
            }
            return Response(response_context, 200)