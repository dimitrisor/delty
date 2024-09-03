from django.http import QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import TemplateView

from delty.actions.check_address_crawlability import check_address_crawlability
from delty.exceptions import ServiceException
from delty.forms.crawling_submission import AddressForm
from delty.views.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        form = AddressForm()
        return render(request, "index.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = AddressForm(request.POST)
        if form.is_valid():
            try:
                url = form.cleaned_data["url"]
                check_address_crawlability.execute(request.user, url)
                full_url = request.build_absolute_uri(
                    f'{reverse("render_url")}?{urlencode({"url": url})}'
                )
            except ServiceException as e:
                form.add_error("url", str(e.detail))
        query = QueryDict(f"rendering_url={full_url}")
        return redirect(f'{reverse("initiate_crawling")}?{query.urlencode()}')
