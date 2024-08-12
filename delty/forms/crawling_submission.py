from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Row, Column, HTML
from django import forms
from django.core.validators import URLValidator
from django.urls import reverse


class AddressForm(forms.Form):
    """
    This form is used for fetching the page.
    """

    url = forms.CharField(
        label="",
        initial="http://in.gr",
        validators=[URLValidator()],
        widget=forms.URLInput(attrs={"placeholder": "Enter a URL"}),
    )
    element_selector = forms.CharField(label="", required=False)

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    FieldWithButtons(
                        Field("url"),
                        StrictButton(
                            "Fetch",
                            type="submit",
                            id="id_fetch",
                            css_class="btn btn-primary",
                            formaction="",
                        ),
                    ),
                    css_class="input-group",
                ),
            )
        )


class CrawlingSubmissionForm(AddressForm):
    """
    This form is used to select an element in the iframe.
    """

    iframe_width = forms.IntegerField(widget=forms.HiddenInput(), required=True)
    iframe_height = forms.IntegerField(widget=forms.HiddenInput(), required=True)

    def __init__(self, *args, **kwargs):
        super(CrawlingSubmissionForm, self).__init__(*args, **kwargs)
        self.helper.layout.extend(
            [
                Row(
                    Column(
                        HTML(
                            "<p>Please select an element in the frame below to observe every day</p>"
                        )
                    )
                ),
                Row(
                    Column(
                        FieldWithButtons(
                            Field(
                                "element_selector",
                                placeholder="No element selector generated.",
                                readonly=True,
                            ),
                            StrictButton(
                                "Crawl",
                                type="submit",
                                id="id_crawl",
                                css_class="btn btn-primary disabled",
                                formaction=reverse("initiate_crawling"),
                            ),
                        ),
                        css_class="input-group",
                    ),
                ),
                Field("iframe_width"),
                Field("iframe_height"),
            ]
        )
        print("CrawlingSubmissionForm")
