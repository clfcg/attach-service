from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample, inline_serializer

from attach.api.serializers import GetViewDataAttachPollSerializer
from attach.models import GetViewDataAttachPoll


@extend_schema(
    tags=["GetViewAttachStart/Poll"]
)
@extend_schema_view(
    post=extend_schema(
        summary="Запросить ссылку на файл",
        description='''По переданному opToken'у передается статус готовности файла (PROCESS, COMPLITE).
        Если файл готов для скачивания передается ссылка на файл в формате .json и запакованый в zip-архив.''',
        request=GetViewDataAttachPollSerializer,
        examples=[
            OpenApiExample(
                "Post example",
                description="Тестовый пример для POST запроса",
                value={
                    'externalRequestId': "16624070-E322-3023-9669-068D20196542",
                    'opToken': "894e3255d211e634ff6011261dfd287w"
                },
                status_codes=[300]
            )
        ],
        responses={
            status.HTTP_200_OK: inline_serializer(
                name='PollProcess',
                fields={
                    'externalRequestId': serializers.CharField(),
                    'status': serializers.CharField()
                }
            ),
            status.HTTP_201_CREATED: inline_serializer(
                name='PollComplite',
                fields={
                    'externalRequestId': serializers.CharField(),
                    'status': serializers.CharField(),
                    'viewAttachFile': serializers.FileField()
                }
            ),
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='ErrorCodeResponsePoll',
                fields={
                    'code': serializers.CharField(),
                    'message': serializers.CharField(),
                }
            )
        },
    ),
)


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