from django.contrib import admin
from .models import *

@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    list_filter = ('author', )
    list_per_page = 20

admin.site.register(PostComment)