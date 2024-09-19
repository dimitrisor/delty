from unittest import mock

import django.test

from delty.services.storage import StorageService
from delty.tasks import TrackContentDifference
from delty.models import ElementSnapshot
from delty.tests.factories.crawling_job import CrawlingJobFactory
from delty.tests.factories.element_snapshot import ElementSnapshotFactory
from delty.tests.factories.page_snapshot import PageSnapshotFactory
from delty.tests.factories.url_address import UrlAddressFactory
from delty.tests.factories.user import UserFactory
from delty.utils import compute_sha256


class TrackContentDifferenceTests(django.test.TestCase):
    @mock.patch.object(StorageService, "upload_message")
    @mock.patch("delty.actions.track_content_difference.fetch_response_fully_loaded")
    def test_execute_when_diff_found(self, mock_fetch_response, mock_upload_message):
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
        mock_upload_message.return_value = "s3://bucket/key"

        user = UserFactory()
        url_address = UrlAddressFactory()
        page_snapshot = PageSnapshotFactory(
            address=url_address, hash=compute_sha256(init_page_content)
        )
        element_snapshot = ElementSnapshotFactory(
            page_snapshot=page_snapshot,
            hash=compute_sha256(init_element_content),
        )
        crawling_job = CrawlingJobFactory(
            user=user, url_address=url_address, latest_element_snapshot=element_snapshot
        )
        crawling_job.element_snapshots.add(element_snapshot)

        expected_new_element_snapshot_hash = compute_sha256(
            '<div class="list_a"><ul><li>hi John</li><li>hi ' "Doe</li></ul></div>"
        )

        TrackContentDifference.execute(crawling_job.user.id, str(crawling_job.id))

        new_element_snapshot = ElementSnapshot.objects.order_by("-version").first()
        crawling_job.refresh_from_db()

        self.assertEqual(crawling_job.latest_element_snapshot, new_element_snapshot)
        self.assertEqual(new_element_snapshot.hash, expected_new_element_snapshot_hash)
        mock_upload_message.assert_called_once_with(
            '<div class="list_a"><ul><li>hi John</li><li>hi Doe</li></ul></div>',
            "88a6a938869d8437dbd0dabda25fccc5f6df4d32960ccaa1c8e0bd1e0456abb7",
        )
