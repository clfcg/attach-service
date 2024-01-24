import re

from django import forms
from drf_api_logger.models import APILogsModel


def api_distinct():
        API_METHOD_REGEX = r'api/(\w+)/'
        distinct_val = set()
        queryset = APILogsModel.objects.values('api').distinct()
        for value in queryset:
            for v in value.values():
                distinct_val.add(re.findall(API_METHOD_REGEX, v)[0])
        distinct_val = tuple(zip(distinct_val, distinct_val))
        return distinct_val


class APILogsForm(forms.Form):
    title = forms.CharField(max_length=50)
    api = forms.ChoiceField(
        label='API метод',
        choices=api_distinct()
    )
        

