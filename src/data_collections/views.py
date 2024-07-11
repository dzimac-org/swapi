from django.http import HttpResponse
from django.views.generic import TemplateView
from data_collections.models import Collection
from rest_framework.decorators import api_view
from rest_framework.response import Response

from etl.swapi.extract.client import SWAPIClient
from etl.swapi.extract.exceptions import SWAPIClientError


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["collections"] = Collection.objects.all()
        print(Collection.objects.all())
        return context


class CollectionDetailView(TemplateView):
    template_name = "collection_detail.html"


@api_view(["POST"])
def fetch(request):
    try:
        api_client = SWAPIClient()
        persons_data = []
        planets_data = []
        # move elsewhere
        for persons, planets in api_client.get_sw_data():
            yield persons, planets

    except SWAPIClientError:
        return Response("Couldn't fetch the data", status=status.HTTP_502_BAD_GATEWAY)