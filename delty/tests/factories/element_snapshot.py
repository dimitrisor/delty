import factory.fuzzy

from delty.models import UrlAddress
from delty.utils import compute_sha256


class ElementSnapshotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UrlAddress

    page_snapshot = None
    selector = "div > .list_a"
    content = "<div><ul><li>hi John</li><li>hi Doe</li></ul></div>"
    hash = compute_sha256(content)
    diff = None
    version = 1
