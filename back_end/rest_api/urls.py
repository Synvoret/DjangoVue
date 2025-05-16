from django.urls import path

from rest_api.views import UserListView

urlpatterns = [
    path("users/", UserListView.as_view(), name="user-list"),
]
