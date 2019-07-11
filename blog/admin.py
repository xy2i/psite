from django.contrib import admin
from .models import Post
from markdownx.admin import MarkdownxModelAdmin


class PostAdmin(MarkdownxModelAdmin):
    list_display = ('title', 'content', 'published_date', 'is_draft', 'slug')
    list_filter = ['published_date']
    search_fields = ['title', 'content']



admin.site.register(Post, PostAdmin)