import datetime

from rest_framework import viewsets
from attach.api.serializers import HislpuSerializer
from attach.models import Histlpu


class HistlpuViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Histlpu.objects.filter(dedit__gte=datetime.date(2023, 11, 20))
    serializer_class = HislpuSerializer