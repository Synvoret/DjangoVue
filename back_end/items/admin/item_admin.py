from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin

from items.models import Item


class ItemResource(resources.ModelResource):
    class Meta:
        model = Item
        fields = ["id", "name", "description", "author", "created_at"]


# CRUD
@admin.register(Item)
class ItemAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ItemResource
    list_display = ["id", "name", "description", "author", "created_at"]
