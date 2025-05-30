from django.urls import include, path
from rest_framework.routers import DefaultRouter

from rest_api.views import BlogView, ItemViewset, UserListView, BlogDetailView

router = DefaultRouter()
router.register(r"items", ItemViewset, basename="item")

urlpatterns = [
    path("users/", UserListView.as_view(), name="user-list"),
    path("", include(router.urls)),
    path("blog/", BlogView.as_view()),
    path("blog/<int:pk>/", BlogDetailView.as_view(), name="blog-detail"),
]
