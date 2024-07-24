from django.shortcuts import render
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import TemplateView

from delty.actions.check_address_crawlability import check_address_crawlability
from delty.exceptions import ServiceException
from delty.forms.adress import AddressForm
from delty.views.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        form = AddressForm()
        return render(request, "index.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = AddressForm(request.POST)
        context = {"form": form}
        if form.is_valid():
            try:
                url = form.cleaned_data["url"]
                check_address_crawlability.execute(url)
                full_url = request.build_absolute_uri(
                    f'{reverse("render_url")}?{urlencode({"url": url})}'
                )
                context["url"] = full_url
            except ServiceException as e:
                form.add_error("url", str(e.detail))
        return render(request, "index.html", context)
