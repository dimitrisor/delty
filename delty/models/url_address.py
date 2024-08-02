from django.db import models

from delty.models.base import BaseModel


class UrlAddress(BaseModel):
    url = models.URLField(unique=True, max_length=2083)
