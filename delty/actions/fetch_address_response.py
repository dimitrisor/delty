import logging

from django.contrib.auth.models import User

from delty.actions.common import fetch_response
from delty.exceptions import ServiceException

logger = logging.getLogger(__name__)


class FetchAddressResponse:
    def execute(self, actor: User, url: str) -> tuple[str, str]:
        try:
            response = fetch_response(url)
            logger.info(
                msg="Successfully fetched address response.",
                extra={"url": url, "actor": actor.id},
            )
            return response
        except ServiceException as e:
            logger.error(
                msg="Failed to fetch address response.",
                extra={
                    "url": url,
                    "actor": actor.id,
                },
            )
            raise e


fetch_address_response = FetchAddressResponse()
