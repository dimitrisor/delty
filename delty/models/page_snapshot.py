from django.db import models
from django.db.models import DO_NOTHING

from delty.models import UrlAddress
from delty.models.base import BaseModel


class PageSnapshot(BaseModel):
    address = models.ForeignKey(
        UrlAddress, on_delete=DO_NOTHING, related_name="page_snapshots"
    )
    hash = models.CharField(max_length=64)
