import time
from datetime import date, datetime, timezone

import freezegun
import petl
from django.forms import model_to_dict
from django.test import TestCase
from petl import MemorySource

from data_collections.models import Collection, SWPerson
from etl.swapi.load.loader import SWAPILoader
from etl.swapi.mocked_swapi_responses import people_mocked_data, planets_mocked_data
from etl.swapi.transform.transform import SWAPITransformTable


class TestSWAPILoader(TestCase):
    @classmethod
    def setUpTestData(cls):
        transformer = SWAPITransformTable(people_mocked_data, planets_mocked_data)
        transformer.transform()
        cls.transformed_table = transformer.result_table

    def test_load_data(self):
        self.assertEqual(Collection.objects.count(), 0)
        self.assertEqual(SWPerson.objects.count(), 0)
        ts = time.time() #yes it's not uuid :/
        loader = SWAPILoader(self.transformed_table, ts)
        loader.load_data()
        self.assertEqual(Collection.objects.count(), 1)
        collection = Collection.objects.get()
        memory_source = MemorySource()
        petl.tocsv(self.transformed_table, memory_source)
        self.assertEqual(collection.file.file.read(), memory_source.getvalue())
        print(collection.file.name)
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
