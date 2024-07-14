import django_filters
from django.db.models import Count

from data_collections.models import SWPerson


class SWPersonFilterSet(django_filters.FilterSet):
    name = django_filters.BooleanFilter()
    birth_year = django_filters.BooleanFilter()
    homeworld = django_filters.BooleanFilter()
    height = django_filters.BooleanFilter()
    mass = django_filters.BooleanFilter()
    hair_color = django_filters.BooleanFilter()
    skin_color = django_filters.BooleanFilter()
    eye_color = django_filters.BooleanFilter()
    gender = django_filters.BooleanFilter()
    date = django_filters.BooleanFilter()

    class Meta:
        model = SWPerson
        fields = []

    def filter_queryset(self, queryset):
        aggregate_fields = [
            name for name, value in self.form.cleaned_data.items() if value
        ]

        if aggregate_fields:
            queryset = queryset.values(*aggregate_fields).annotate(count=Count("id"))

        return queryset
