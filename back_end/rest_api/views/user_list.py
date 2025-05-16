from django.contrib.auth.models import User
from rest_framework import generics

from rest_api.serializers import UserSerializer


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
