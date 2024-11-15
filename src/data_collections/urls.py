from django.urls import path

from data_collections.views import (CollectionAggregateView,
                                    CollectionListView,
                                    CollectionPersonsListView, fetch)

urlpatterns = [
    path("", CollectionListView.as_view(), name="collections-list"),
    path(
        "collections/<int:pk>/",
        CollectionPersonsListView.as_view(),
        name="collections-persons",
    ),
    path(
        "collection/<int:pk>/aggregate",
        CollectionAggregateView.as_view(),
        name="collections-aggregate",
    ),
    path("fetch/", fetch),
]
