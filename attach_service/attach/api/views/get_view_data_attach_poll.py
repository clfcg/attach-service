from rest_framework.views import APIView
from rest_framework.response import Response

from attach.api.serializers import GetViewDataAttachPollSerializer
from attach.models import GetViewDataAttachPoll


class GetViewDataAttachPollView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = GetViewDataAttachPollSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            poll_file = GetViewDataAttachPoll.objects.get(op_token=serializer.data['opToken'])
            poll_file.external_request_id = serializer.data['externalRequestId']
            poll_file.save()

            response_context = {
                "externalRequestId": serializer.data['externalRequestId'],
                "status": poll_file.status,
            }
            if poll_file.status == 'COMPLITE':
                file_url = "http://" + request.headers["Host"] + poll_file.poll_file.url
                response_context["viewAttachFile"] = file_url
                return Response(response_context, 201)
            else:
                return Response(response_context, 200)