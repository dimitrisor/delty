from django.urls import path

from delty.views.auth import register, login
from delty.views.crawler import RenderURLView
from delty.views.crawler import CrawlerView
from delty.views.index import IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("render_url", RenderURLView.as_view(), name="render_url"),
    path("initiate_crawilng", CrawlerView.as_view(), name="initiate_crawilng"),
    path("register", register, name="register"),
    path("login", login, name="login"),
]
