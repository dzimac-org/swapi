from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from data_collections.models import Collection, SWPerson

basic_sw_person_data = {
    "name": "Luke",
    "birth_year": "100",
    "homeworld": "",
    "height": "",
    "mass": "",
    "hair_color": "",
    "skin_color": "",
    "eye_color": "",
    "gender": "",
    "date": "2000-10-10",
}


class TestAggregateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.collection = Collection.objects.create(file="file1.csv")
        cls.collection_2 = Collection.objects.create(file="file2.csv")

        for collection in [cls.collection, cls.collection_2]: # assign same items to two collections
            sw_person_data = basic_sw_person_data.copy()
            sw_person_data["collection_id"] = collection.id
            for _ in range(2):
                SWPerson.objects.create(**sw_person_data)
            sw_person_data |= {"birth_year": "200"}
            SWPerson.objects.create(**sw_person_data)
            sw_person_data |= {"name": "Random", "birth_year": "1000"}
            SWPerson.objects.create(**sw_person_data)



    def test_aggregation_by_name(self):
        url = f"{reverse('collections-aggregate', args=[self.collection.pk])}?name=True"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # created 3 Luke's and 1 Random PER collection
        self.assertContains(
            response,
            "<td>Luke</td><td>3</td>",
            status_code=status.HTTP_200_OK,
            html=True,
        )
        self.assertContains(
            response,
            "<td>Random</td><td>1</td>",
            status_code=status.HTTP_200_OK,
            html=True,
        )
