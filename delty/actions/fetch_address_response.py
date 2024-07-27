from delty.actions.common import fetch_response


class FetchAddressResponse:
    def execute(self, url: str) -> tuple[str, str]:
        return fetch_response(url)


fetch_address_response = FetchAddressResponse()
