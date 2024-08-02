import factory.fuzzy

from delty.models import UrlAddress


class UrlAddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UrlAddress

    url = factory.Faker("url")
