from django.contrib import admin
from django.core.exceptions import ValidationError
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget

from items.models import Item
from profiles.models import Profile


class ItemResource(resources.ModelResource):
    author = fields.Field(
        column_name="author",
        attribute="author",
        widget=ForeignKeyWidget(Profile, field="id"),
    )

    class Meta:
        model = Item
        fields = ["id", "name", "description", "author", "created_at"]
        skip_unchanged = True
        report_skipped = True

    def before_import_row(self, row, **kwargs):
        # validate length name
        name = row.get("name")
        if name and len(name) > 500:
            raise ValidationError(f"Name '{name}' is too long (max 500 letters).")

        # check author exists
        author_id = row.get("author")
        if author_id:
            try:
                Profile.objects.get(id=author_id)
            except Profile.DoesNotExist:
                raise ValidationError(f"Author o ID {author_id} doesn't exists.")


@admin.register(Item)
class ItemAdmin(ImportExportModelAdmin):
    resource_class = ItemResource
    list_display = ["id", "name", "description", "author", "created_at"]
    list_filter = ["author", "created_at"]
    search_fields = ["name", "description"]
