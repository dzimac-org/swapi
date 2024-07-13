from abc import ABC, abstractmethod
from typing import Dict, Union

import requests
from django.conf import settings
from requests import Response
from rest_framework import status

from etl.swapi.extract.exceptions import (
    SWAPIConnectionError,
    SWAPIResponseDataError,
    SWAPIResponseStatusError,
)


class APIClient(ABC):
    @abstractmethod
    def api_url(self) -> str:
        """Returns the API url"""

    def make_request(self, method, url) -> Response:
        """Make a request with given method to the api_url"""

    def handle_response(self, response) -> Union[Dict[str, any], None]:
        """Handle response depending on the returned status"""


class SWAPIClient(APIClient):
    api_url = settings.SWAPI_URL

    def make_request(self, method, url) -> Response:
        try:
            response = getattr(requests, method)(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise SWAPIConnectionError(str(e))
        return response

    def handle_response(self, response) -> Union[Dict[str, any], None]:
        if response.status_code != status.HTTP_200_OK:
            raise SWAPIResponseStatusError(status_code=response.status_code)

        try:
            json_data = response.json()
        except ValueError as e:
            raise SWAPIResponseDataError(
                f"Error while parsing response to JSON. Error: {str(e)}"
            )

        return json_data

    def get_data(self, url) -> list[Dict[str, any]]:
        while url:
            response = self.make_request("get", url=url)
            json_data = self.handle_response(response)
            yield json_data["results"]
            url = json_data["next"]

    def get_planets_mapping(self) -> Dict[str, str]:
        planets_map = {}
        for planets in self.get_data(self.api_url + "planets/"):
            planets_map.update({i["url"]: i["name"] for i in planets})
        return planets_map

    def get_people_data(self):
        yield from self.get_data(self.api_url + "people/")
