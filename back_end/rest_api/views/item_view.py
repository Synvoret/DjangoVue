from rest_framework import viewsets

from items.models import Item
from rest_api.serializers import ItemSerializer


class ItemViewset(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
