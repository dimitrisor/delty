from unittest import mock

import django.test

from delty.actions.track_difference import TrackDifference
from delty.tests.factories.crawling_job import CrawlingJobFactory
from delty.tests.factories.element_snapshot import ElementSnapshotFactory
from delty.tests.factories.user import UserFactory


class TrackDifferenceTests(django.test.TestCase):
    @mock.patch("delty.actions.track_difference.fetch_response")
    def test_execute_when_diff_found(self, mock_fetch_response):
        mock_fetch_response.return_value = (
            "<html><body><h1>Test</h1></body></html>",
            "text/html",
        )
        UserFactory()
        cj = CrawlingJobFactory()
        ElementSnapshotFactory(content="<html><body><h1>Test2</h1></body></html>")
        TrackDifference().execute(cj.user, cj)
        pass
