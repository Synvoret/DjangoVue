from rest_framework import serializers

from blog.models import Post

from .tag_serializer import TagSerializer


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
