from django.urls import path

from data_collections.views import CollectionDetailView, IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path(
        "collections/<int:pk>/",
        CollectionDetailView.as_view(),
        name="collections-detail",
    ),
]
