import re
from datetime import date, timedelta, datetime

from django import forms
from drf_api_logger.models import APILogsModel


def api_distinct():
        API_METHOD_REGEX = r'api/(\w+)/'
        distinct_val = set()
        queryset = APILogsModel.objects.values('api').distinct()
        for value in queryset:
            for v in value.values():
                distinct_val.add(re.findall(API_METHOD_REGEX, v)[0])
        distinct_val = list(zip(distinct_val, distinct_val))
        distinct_val.insert(0, ('', '---------'))
        return distinct_val


def request_date():
    today = date.today().strftime('%Y%m%d')
    week = (date.today() - timedelta(days=7)).strftime('%Y%m%d')
    month = date.today().replace(day=1).strftime('%Y%m%d')
    year = date.today().replace(month=1).replace(day=1).strftime('%Y%m%d')
    period = [
        ('', '---------'),
        (f'{today}/{today}', 'Сегодня'),
        (f'{week}/{today}', 'Последнии 7 дней'),
        (f'{month}/{today}', 'Этот месяц'),
        (f'{year}/{today}', 'Этот год'),
    ]
    return period


def date_parser(val):
    d_beg, d_end = val.split('/')
    d_beg = datetime.strptime(d_beg, '%Y%m%d')
    d_end = datetime.strptime(d_end, '%Y%m%d')
    return (d_beg, d_end)


class APILogsForm(forms.Form):
    api_name = forms.ChoiceField(
        required=False,
        choices=api_distinct,
        widget=forms.Select(
             attrs={
                  'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
             }
        )
    )
    period = forms.TypedChoiceField(
        coerce=date_parser,
        choices=request_date,
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }
        )
    )
    d_beg = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }
        )

    )
    d_end = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }
        )

    )
        

