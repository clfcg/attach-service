from secrets import token_hex

from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema_view, extend_schema, inline_serializer, OpenApiExample

from attach.api.serializers import GetViewDataAttachStartSerializer
from attach.models import GetViewDataAttachStart, GetViewDataAttachPoll
from attach.tasks import generate_attach_file

@extend_schema(
    tags=["GetViewAttachStart/Poll"]
)
@extend_schema_view(
    post=extend_schema(
        summary="Запросить сведения о прикреплениях на дату",
        description='''При корректной отправке запроса начинается формирование файла прикреплений на указанную дату. 
        В ответ приходит токен, по которому можно запросить сформированный файл.''',
        request=GetViewDataAttachStartSerializer,
        examples=[
            OpenApiExample(
                "Post example",
                description="Тестовый пример для POST запроса",
                value={
                    'externalRequestId': "16624070-E322-3023-9669-068D20196542",
                    'dateQuery': "2023-12-05"
                },
                status_codes=[300]
            )
        ],
        responses={
            status.HTTP_200_OK: inline_serializer(
                name='Success',
                fields={
                    'externalRequestId': serializers.CharField(),
                    'opToken': serializers.CharField()
                }
            ),
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='ErrorCodeResponseStart',
                fields={
                    'code': serializers.CharField(),
                    'message': serializers.CharField(),
                }
            )
        },
    ),
)


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