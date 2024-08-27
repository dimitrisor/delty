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
    selector = factory.fuzzy.FuzzyText()
    iframe_width = 1920
    iframe_height = 1080
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    status = factory.fuzzy.FuzzyChoice(CrawlingJob.Status.values)
    submitted_at = factory.LazyFunction(timezone.now)
