from datetime import datetime

import petl
from django.utils.functional import classproperty


class SWAPITransformTable:
    @classproperty
    def columns_to_drop(self):
        return ["films", "species", "vehicles", "starships", "created", "url"]

    def __init__(self, persons_data: list[dict], planets_map):
        self.persons_table = petl.fromdicts(persons_data)
        self.planets_map = planets_map
        self.result_table = None

    def parse_edited_data(self):
        self.persons_table = petl.convert(
            self.persons_table,
            "edited",
            lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ").strftime(
                "%Y-%m-%d"
            ),
        )

    def rename_edited_column(self):
        self.persons_table = petl.rename(self.persons_table, "edited", "date")

    def drop_not_needed_columns(self):
        self.persons_table = self.persons_table.cutout(*self.columns_to_drop)

    def resolve_planet_hyperlink_into_name(self):
        self.persons_table = petl.convert(
            self.persons_table,
            "homeworld",
            lambda x: self.planets_map.get(x, "")
        )

        print("resolve")
        print(petl.header(self.persons_table))

    def transform(self):
        self.parse_edited_data()
        self.rename_edited_column()
        self.drop_not_needed_columns()
        self.resolve_planet_hyperlink_into_name()
        return self.persons_table
