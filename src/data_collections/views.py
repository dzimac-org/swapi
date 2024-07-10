from django.views.generic import TemplateView

from data_collections.models import Collection


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["collections"] = Collection.objects.all()
        print(Collection.objects.all())
        return context


class CollectionDetailView(TemplateView):
    template_name = "collection_detail.html"