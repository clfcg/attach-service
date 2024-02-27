from datetime import datetime
from typing import Any
from django.db.models.query import QuerySet

from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import DateField
from django.db.models.functions import Cast
from django.views.generic.list import ListView

from .forms import APILogsForm
from drf_api_logger.models import APILogsModel


# Create your views here.
def index(request):
    return render(request, "attach/index.html")


def api_log(request):
    if request.method == 'POST':
        form = APILogsForm(request.POST)
        if form.is_valid():
            # cd = form.cleaned_data
            # queryset = APILogsModel.objects.order_by('-added_on')
            # if cd['api_name'] != '':
            #     queryset = queryset.filter(api__contains=form.cleaned_data['api_name'])
            # if cd['period'] != '':
            #     queryset = queryset.annotate(
            #         date_log = Cast('added_on', output_field=DateField())
            #     ).filter(date_log__range=(cd['period'][0], cd['period'][1]))
            # if cd['period'] == '' and cd['d_beg'] is not None and cd['d_end'] is not None:
            #     queryset = queryset.annotate(
            #         date_log = Cast('added_on', output_field=DateField())
            #     ).filter(date_log__range=(cd['d_beg'], cd['d_end']))
            # queryset = queryset.order_by('-added_on')
            # context = {
            #     'form': form,
            #     'data': queryset,
            # }
            # print(cd)
            return render(request, 'attach/api_search.html', {'form': form})
    else:
        form = APILogsForm()
        return render(request, 'attach/api_search.html', {'form': form})


def api_logs_table_view(request):
    queryset = APILogsModel.objects.all()
    paginator = Paginator(queryset, 15)
    page_number = request.GET.get('page')
    obj = paginator.get_page(page_number)
    

    return render(request, 'attach/api_logs.html', {'data': obj})
    