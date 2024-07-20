# Register your models here.
from django.contrib import admin
from delty.models import UrlAddress, PageSnapshot, SelectedElement, CrawlingJob

admin.site.register(UrlAddress)
admin.site.register(PageSnapshot)
admin.site.register(SelectedElement)
admin.site.register(CrawlingJob)
