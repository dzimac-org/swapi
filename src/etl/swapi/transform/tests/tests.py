from unittest.mock import patch

import petl
from django.test import TestCase

from etl.swapi.mocked_swapi_responses import (people_mocked_data,
                                              planets_mocked_data)
from etl.swapi.transform.transform import SWAPITransformTable


class TestSWAPITransformTable(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.transform_class = SWAPITransformTable(
            people_mocked_data, planets_mocked_data
        )

    def test_parse_edited_data(self):
        self.transform_class.parse_edited_data()
        self.assertEqual(
            petl.values(self.transform_class.persons_table, "edited")[0], "2014-12-20"
        )

    def test_rename_edited_column(self):
        self.transform_class.rename_edited_column()
        self.assertIn("date", self.transform_class.persons_table.fieldnames())
        self.assertNotIn("edited", self.transform_class.persons_table.fieldnames())

    def test_drop_not_needed_columns(self):
        self.transform_class.drop_not_needed_columns()
        for column in SWAPITransformTable.columns_to_drop:
            self.assertNotIn(column, self.transform_class.persons_table.fieldnames())

    def test_resolve_planet_hyperlink_into_name(self):
        self.transform_class.resolve_planet_hyperlink_into_name()
        self.assertEqual(
            petl.values(self.transform_class.result_table, "homeworld")[0], "Tatooine"
        )

    @patch.object(SWAPITransformTable, "resolve_planet_hyperlink_into_name")
    @patch.object(SWAPITransformTable, "drop_not_needed_columns")
    @patch.object(SWAPITransformTable, "rename_edited_column")
    @patch.object(SWAPITransformTable, "parse_edited_data")
    def test_transform_method_calls(
        self, mocked_parse, mocked_rename, mocked_drop, mocked_resolve
    ):
        self.transform_class.transform()

        mocked_parse.assert_called_once()
        mocked_rename.assert_called_once()
        mocked_drop.assert_called_once()
        mocked_resolve.assert_called_once()
