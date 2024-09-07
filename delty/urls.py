from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from django.contrib import admin
from delty.views.auth import register, login
from delty.views.crawler import RenderURLView
from delty.views.crawler import CrawlerView
from delty.views.index import IndexView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", IndexView.as_view(), name="index"),
    path("render_url", RenderURLView.as_view(), name="render_url"),
    path("initiate_crawling", CrawlerView.as_view(), name="initiate_crawling"),
    path("register", register, name="register"),
    path("login", login, name="login"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0]
    )
