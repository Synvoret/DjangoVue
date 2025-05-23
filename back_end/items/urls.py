from django.urls import path

from items.views import items_export

urlpatterns = [
    path("export/", items_export, name="items_export"),
]
