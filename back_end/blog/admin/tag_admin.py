from django.contrib import admin

from blog.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag
