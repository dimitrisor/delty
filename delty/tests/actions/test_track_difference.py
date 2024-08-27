from unittest import mock

import django.test

from delty.actions.track_difference import track_difference
from delty.models import ElementSnapshot
from delty.tests.factories.crawling_job import CrawlingJobFactory
from delty.tests.factories.element_snapshot import ElementSnapshotFactory
from delty.tests.factories.page_snapshot import PageSnapshotFactory
from delty.tests.factories.url_address import UrlAddressFactory
from delty.tests.factories.user import UserFactory
from delty.utils import compute_sha256


class TrackDifferenceTests(django.test.TestCase):
    @mock.patch("delty.actions.track_difference.fetch_response_fully_loaded")
    def test_execute_when_diff_found(self, mock_fetch_response):
        init_page_content = '<html><body><div class="list_a"><ul><li>hi John</li></ul></div></body></html>'
        init_element_content = (
            '<div class="list_a"><ul><li>hi John</li></ul></div></body></html>'
        )
        new_page_content = (
            '<html><body><div class="list_a"><ul><li>hi John</li><li>hi '
            "Doe</li></ul></div></body></html>"
        )

        mock_fetch_response.return_value = (
            new_page_content,
            "text/html",
        )
        user = UserFactory()
        url_address = UrlAddressFactory()
        page_snapshot = PageSnapshotFactory(
            address=url_address, hash=compute_sha256(init_page_content)
        )
        element_snapshot = ElementSnapshotFactory(
            page_snapshot=page_snapshot,
            content=init_element_content,
            hash=compute_sha256(init_element_content),
        )
        crawling_job = CrawlingJobFactory(
            user=user, url_address=url_address, latest_element_snapshot=element_snapshot
        )
        crawling_job.element_snapshots.add(element_snapshot)

        track_difference.execute(crawling_job.user, crawling_job)

        new_element_snapshot = ElementSnapshot.objects.order_by("-version").first()

        self.assertEqual(crawling_job.latest_element_snapshot, new_element_snapshot)
        self.assertEqual(
            new_element_snapshot.content,
            '<div class="list_a"><ul><li>hi John</li><li>hi Doe</li></ul></div>',
        )
