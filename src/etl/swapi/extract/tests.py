from unittest.mock import MagicMock, Mock, patch

import requests
from django.test import TestCase
from rest_framework import status

from etl.swapi.extract.client import SWAPIClient
from etl.swapi.extract.exceptions import (SWAPIConnectionError,
                                          SWAPIResponseDataError,
                                          SWAPIResponseStatusError)


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

        result = self.swapi_client.get_all_data("test")
        self.assertEqual(result, response_data["results"])

    @patch("etl.swapi.extract.client.requests.get")
    def test_make_request_response_status_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.side_effect = yield from [mock_response]

        with self.assertRaises(SWAPIResponseStatusError):
            self.swapi_client.get_all_data("test")

    @patch("etl.swapi.extract.client.requests.get")
    def test_make_request_connection_error(self, mock_get):
        mock_get.side_effect = yield from [requests.exceptions.RequestException("Request error")]
        with self.assertRaises(SWAPIConnectionError):
            self.swapi_client.get_all_data("test")

    @patch("etl.swapi.extract.client.requests.get")
    def test_make_request_json_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("JSON parsing error")
        mock_get.side_effect = yield from [mock_response]
        with self.assertRaises(SWAPIResponseDataError):
            self.swapi_client.get_all_data("test")

    @patch("requests.get")
    def test_get_all_data(self, mocked_get):
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
        for response in self.swapi_client.get_all_data("http://test.com"):
            result.extend(response)
        self.assertEqual(result, [{"name": "Luke Skywalker"}, {"name": "Darth Vader"}])
        self.assertEqual(mocked_get.call_count, 2)

    @patch.object(SWAPIClient, "get_all_data")
    def test_get_sw_data(self, mock_get_all_data):
        mock_persons, mock_planets = yield(Mock(), Mock())
        mock_get_all_data.side_effect = [mock_persons, mock_planets]

        persons = []
        planets = []
        for response_persons, response_planets in self.swapi_client.get_sw_data():
            persons.extend(response_persons)
            planets.extend(response_planets)

        self.assertEqual([persons, planets], [mock_persons, mock_planets])

        expected_people_url = self.swapi_client.api_url + "people/"
        expected_planets_url = self.swapi_client.api_url + "planets/"

        mock_get_all_data.assert_any_call(expected_people_url)
        mock_get_all_data.assert_any_call(expected_planets_url)
        self.assertEqual(mock_get_all_data.call_count, 2)