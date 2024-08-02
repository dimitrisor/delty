import factory.fuzzy
from django.utils import timezone

from delty.models import CrawlingJob


class CrawlingJobFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CrawlingJob

    user = factory.SubFactory("delty.tests.factories.user.UserFactory")
    url_address = factory.SubFactory(
        "delty.tests.factories.url_address.UrlAddressFactory"
    )
    latest_element_snapshot = factory.SubFactory(
        "delty.tests.factories.element_snapshot.ElementSnapshotFactory"
    )
    status = factory.fuzzy.FuzzyChoice(CrawlingJob.Status.values)
    submitted_at = factory.LazyFunction(timezone.now)
