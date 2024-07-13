from data_collections.models import Collection
from etl.base_etl import ETL
from etl.swapi.extract.client import SWAPIClient
from etl.swapi.load.loader import SWAPILoader
from etl.swapi.transform.transform import SWAPITransformTable
from time import time
from typing import List, Union


class SWAPIETL(ETL):

    api_client: SWAPIClient
    ts: int
    create_csv: bool
    collection: Union[Collection, bool]
    planets_data: List

    def before_etl(self):
        self.api_client = SWAPIClient()
        self.create_csv = True
        self.collection = None
        self.ts = time()
        self.planets_data = self.api_client.get_planets_mapping()

    def extract(self):
        yield from self.api_client.get_people_data()

    def transform(self, data):
        transform_cls = SWAPITransformTable(data, self.planets_data)
        return transform_cls.transform()

    def load(self, transformed_data):
        loader = SWAPILoader(
            transformed_data, self.ts, self.create_csv, self.collection
        )
        loader.load_data()
        self.collection = loader.collection
        self.create_csv = False

    def after_etl(self):
        pass
