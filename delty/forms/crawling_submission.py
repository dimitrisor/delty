from django import forms
from django.core.validators import URLValidator


class CrawlingSubmissionForm(forms.Form):
    url = forms.CharField(validators=[URLValidator()])
    element_selector = forms.CharField(label="")
