from abc import ABC, abstractmethod


class ETL(ABC):
    @abstractmethod
    def extract(self):
        """Extract data"""

    @abstractmethod
    def transform(self):
        """Transform data"""

    @abstractmethod
    def load(self):
        """Load data"""

    def process(self):
        self.extract()
        self.transform()
        self.load()
