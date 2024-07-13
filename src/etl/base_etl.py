from abc import ABC, abstractmethod


class ETL(ABC):

    @abstractmethod
    def before_etl(self):
        """Before ETL"""

    @abstractmethod
    def extract(self):
        """Extract data"""

    @abstractmethod
    def transform(self):
        """Transform data"""

    @abstractmethod
    def load(self):
        """Load data"""

    @abstractmethod
    def after_etl(self):
        """After ETL"""

    def process(self):
        """General idea"""
        self.before_etl()
        for data in self.extract():
            transformed_data = self.transform(data)
            self.load(transformed_data)
        self.after_etl()
