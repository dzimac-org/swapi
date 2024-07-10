from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from data_collections.models import Collection
from freezegun import freeze_time


class CollectionModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        file = SimpleUploadedFile(
            "ttswapi.csv",
            content=b"name,height,mass\nLuuuuuke,180,75",
            content_type="text/csv",
        )
        cls.collection = Collection.objects.create(file=file)

    def test_create_collection(self):
        self.assertIsNotNone(self.collection.file)
        self.assertIsNotNone(self.collection.created)

    def test_ordering(self):
        with freeze_time("2024-01-01"):  # older
            second_file = SimpleUploadedFile(
                "ttswapi2.csv",
                content=b"name,height,mass\nLuuuuuke,180,75",
                content_type="text/csv",
            )
        collection_2 = Collection.objects.create(file=second_file)
        collections = Collection.objects.all()

        self.assertListEqual(
            [collections[0], collections[1]], [collection_2, self.collection]
        )