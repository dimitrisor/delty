import logging


from delty.actions.common import fetch_response
from delty.exceptions import ServiceException

logger = logging.getLogger(__name__)


class FetchAddressResponse:
    def execute(self, url: str) -> tuple[str, str]:
        try:
            return fetch_response(url)
        except ServiceException as e:
            logger.error(
                msg="Failed to fetch address response.",
                extra={
                    "url": url,
                },
            )
            raise e


fetch_address_response = FetchAddressResponse()
