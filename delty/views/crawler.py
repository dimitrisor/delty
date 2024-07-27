from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import View

from delty.errors import WebPageUnreachable
from delty.exceptions import ServiceException
from delty.actions.fetch_address_response import fetch_address_response
from delty.actions.initiate_element_crawling import initiate_element_crawling
from delty.forms.crawling_submission import CrawlingSubmissionForm
from delty.views.mixins import LoginRequiredMixin


class CrawlerView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = CrawlingSubmissionForm(request.POST)
        if form.is_valid():
            try:
                url = form.cleaned_data["url"]
                element_selector = form.cleaned_data["element_selector"]
                initiate_element_crawling.execute(request.user, url, element_selector)
            except ServiceException as e:
                form.add_error("url", str(e.detail))
        return redirect("index")


class RenderURLView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            url = request.GET.get("url")
            text, content_type = fetch_address_response.execute(url)
            return HttpResponse(text, content_type=content_type)
        except WebPageUnreachable as e:
            return HttpResponse(e.detail, status=e.status_code)
