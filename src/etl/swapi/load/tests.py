import time
from datetime import date, datetime, timezone

import freezegun
import petl
from django.forms import model_to_dict
from django.test import TestCase
from petl import MemorySource

from data_collections.models import Collection, SWPerson
from etl.swapi.load.loader import SWAPILoader
from etl.swapi.mocked_swapi_responses import (people_mocked_data,
                                              planets_mapping)
from etl.swapi.transform.transform import SWAPITransformTable


class TestSWAPILoader(TestCase):
    @classmethod
    def setUpTestData(cls):
        transformer = SWAPITransformTable(people_mocked_data, planets_mapping)
        cls.transformed_data = transformer.transform()

    def test_load_data(self):
        self.assertEqual(Collection.objects.count(), 0)
        self.assertEqual(SWPerson.objects.count(), 0)
        ts = time.time()
        loader = SWAPILoader(self.transformed_data, ts)
        loader.load_data()
        self.assertEqual(Collection.objects.count(), 1)

        collection = Collection.objects.get()

        self.assertIn(
            f"collection_{ts}",
            collection.file.name,
        )

        self.assertEqual(SWPerson.objects.count(), 10)
        swperson = SWPerson.objects.first()
        expected_dict = {
            "id": swperson.id,
            "name": "Luke Skywalker",
            "height": "172",
            "mass": "77",
            "hair_color": "blond",
            "skin_color": "fair",
            "eye_color": "blue",
            "birth_year": "19BBY",
            "gender": "male",
            "homeworld": "Tatooine",
            "date": date(2014, 12, 20),
            "collection": swperson.collection.id,
        }
        self.assertDictEqual(model_to_dict(swperson), expected_dict)
