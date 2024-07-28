# Register your models here.
from django.contrib import admin
from delty.models import UrlAddress, PageSnapshot, ElementSnapshot, CrawlingJob

admin.site.register(UrlAddress)
admin.site.register(PageSnapshot)
admin.site.register(ElementSnapshot)
admin.site.register(CrawlingJob)
