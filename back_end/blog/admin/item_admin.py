from django.contrib import admin

from blog.models import Item


# CRUD
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    model = Item
    list_display = ["id", "name", "description", "author"]
