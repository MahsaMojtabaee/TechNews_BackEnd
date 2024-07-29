from django.contrib import admin
from .models import Tag, News


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'body', 'get_tags', 'resources']

    def get_tags(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()])
