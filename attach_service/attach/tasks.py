import dramatiq
from datetime import datetime
import time
import json

from django.conf import settings
from django.db.models import Q
from .models import People, Histlpu, GetViewDataAttachPoll


@dramatiq.actor
def generate_attach_file(op_token, date_query):
    attach_data = People.objects.filter(dbeg__lt=date_query).filter(Q(dstop__gt=date_query) | Q(dstop__isnull=True))
    attach_data = attach_data.extra(select={"dbeg": "convert(varchar, dbeg, 23)"})
    datas = list(attach_data.values('enp', 'ss', 'dbeg', 'q'))

    fl = settings.BASE_DIR / 'sample.json'

    with open(fl, 'w') as f:
        json.dump(datas, f, indent=4)