from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if 'externalRequestId' in context['request'].data.keys():
            response.data['externalRequestId'] = context['request'].data['externalRequestId']
        if 'externalRequestId' in context['request'].query_params.keys():
            response.data['externalRequestId'] = context['request'].query_params['externalRequestId']
        response.data['code'] = exc.default_code
        response.data['message'] = response.data['detail']
        del response.data['detail']
    return response