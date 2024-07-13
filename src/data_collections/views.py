from django.views.generic import TemplateView, ListView
from data_collections.models import Collection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from etl.swapi.etl import SWAPIETL
from etl.swapi.extract.exceptions import SWAPIClientError


class CollectionListView(ListView):
    model = Collection


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["collections"] = Collection.objects.all()
        return context


class CollectionDetailView(TemplateView):
    template_name = "data_collections/collection_detail.html"


@api_view(["POST"])
def fetch(request):
    try:
        SWAPIETL().process()
    except SWAPIClientError:
        return Response("Couldn't fetch the data", status=status.HTTP_502_BAD_GATEWAY)
    return Response("Data collection created.", status=status.HTTP_200_OK)
