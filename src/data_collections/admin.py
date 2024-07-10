from django.contrib import admin

from data_collections.models import Collection


class CollectionsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Collection, CollectionsAdmin)
