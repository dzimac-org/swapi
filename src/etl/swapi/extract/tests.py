from unittest.mock import MagicMock, Mock, patch

import requests
from django.test import TestCase
from rest_framework import status
from etl.swapi.extract.client import SWAPIClient
from etl.swapi.extract.exceptions import (
    SWAPIConnectionError,
    SWAPIResponseDataError,
    SWAPIResponseStatusError,
)
from etl.swapi.mocked_swapi_responses import planets_mocked_data


class TestSWAPIClient(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.swapi_client = SWAPIClient()

    @patch("etl.swapi.extract.client.requests.get")
    def test_make_request_success(self, mock_get):
        response_data = {"results": [{"key": "value"}], "next": None}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = response_data
        mock_get.side_effect = yield from [mock_response]

        result = self.swapi_client.get_data("test")
        self.assertEqual(result, response_data["results"])

    @patch("etl.swapi.extract.client.requests.get")
    def test_make_request_response_status_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.side_effect = yield from [mock_response]

        with self.assertRaises(SWAPIResponseStatusError):
            self.swapi_client.get_data("test")

    @patch("etl.swapi.extract.client.requests.get")
    def test_make_request_connection_error(self, mock_get):
        mock_get.side_effect = yield from [
            requests.exceptions.RequestException("Request error")
        ]
        with self.assertRaises(SWAPIConnectionError):
            self.swapi_client.get_data("test")

    @patch("etl.swapi.extract.client.requests.get")
    def test_make_request_json_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("JSON parsing error")
        mock_get.side_effect = yield from [mock_response]
        with self.assertRaises(SWAPIResponseDataError):
            self.swapi_client.get_data("test")

    @patch("etl.swapi.extract.client.requests.get")
    def test_get_people_data(self, mocked_get):
        mock_response1 = Mock()
        mock_response1.status_code = status.HTTP_200_OK
        mock_response1.json.return_value = {
            "results": [{"name": "Luke Skywalker"}],
            "next": "https://some-sample-url.com/?page=2",
        }

        mock_response2 = Mock()
        mock_response2.status_code = status.HTTP_200_OK
        mock_response2.json.return_value = {
            "results": [{"name": "Darth Vader"}],
            "next": None,
        }

        mocked_get.side_effect = [mock_response1, mock_response2]
        result = []
        for response in self.swapi_client.get_people_data():
            result.extend(response)
        self.assertEqual(result, [{"name": "Luke Skywalker"}, {"name": "Darth Vader"}])
        self.assertEqual(mocked_get.call_count, 2)

    @patch("etl.swapi.extract.client.requests.get")
    def test_get_planets_mapping(self, mock_get):
        response_data = {"results": planets_mocked_data, "next": None}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = response_data
        mock_get.side_effect = [mock_response]
        result = self.swapi_client.get_planets_mapping()
        self.assertDictEqual(
            result,
            {
                "https://swapi.dev/api/planets/1/": "Tatooine",
                "https://swapi.dev/api/planets/2/": "Alderaan",
                "https://swapi.dev/api/planets/7/": "Endor",
                "https://swapi.dev/api/planets/8/": "Naboo",
                "https://swapi.dev/api/planets/20/": "Stewjon",
            },
        )
