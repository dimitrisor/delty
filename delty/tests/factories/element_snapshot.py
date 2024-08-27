import factory.fuzzy

from delty.models import ElementSnapshot
from delty.tests.factories.page_snapshot import PageSnapshotFactory


class ElementSnapshotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ElementSnapshot

    page_snapshot = factory.SubFactory(PageSnapshotFactory)
    crawling_job = None
    selector = "body > .list_a"
    content = "<ul><li>hi John</li><li>hi Doe</li></ul>"
    hash = factory.Faker("md5")
    diff = None
    version = 1
    content_path = factory.Faker("url")
