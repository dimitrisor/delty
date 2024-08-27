import factory.fuzzy

from delty.models import PageSnapshot
from delty.tests.factories.url_address import UrlAddressFactory


class PageSnapshotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PageSnapshot

    address = factory.SubFactory(UrlAddressFactory)
    hash = factory.Faker("md5")
