from functools import cached_property
from rest_framework.generics import get_object_or_404
from django.views.generic import ListView
from data_collections.models import Collection, SWPerson
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from etl.swapi.etl import SWAPIETL
from etl.swapi.extract.exceptions import SWAPIClientError


class CollectionListView(ListView):
    model = Collection


class CollectionPersonsListView(ListView):
    model = SWPerson
    context_object_name = "persons"
    template_name = "data_collections/collection_persons.html"
    paginate_by = 10

    @cached_property
    def collection(self):
        return get_object_or_404(Collection, pk=self.kwargs.get("pk"))

    def get_queryset(self):
        return self.collection.persons.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["collection_file_name"] = self.collection.file.name
        return context


@api_view(["POST"])
def fetch(request):
    try:
        SWAPIETL().process()
    except SWAPIClientError:
        return Response("Couldn't fetch the data", status=status.HTTP_502_BAD_GATEWAY)
    return Response("Data collection created.", status=status.HTTP_200_OK)
