from django.contrib import admin
from django.urls import include,path
from data_collections.views import (CollectionListView,fetch)

urlpatterns = [
    path("", CollectionListView.as_view(), name="collections-list"),
    path("fetch_collection/", fetch, name="collections-fetch"),
    path("admin/", admin.site.urls),
]

