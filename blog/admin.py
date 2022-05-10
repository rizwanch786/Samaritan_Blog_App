from django.contrib import admin
from .models import *
from django.utils.html import format_html
@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    
    # # # Show fields
    # # fields = ('title',)
    
    # # # Hide fields
    # exclude = ('title',)
    
    # Display fields
    list_display = ('id', 'title', 'less_content', 'click_me','visible')
    
    # # Link other fields to make clickable
    # list_display_links = ('id', 'title', 'less_content', 'click_me', 'visible')
    
    # Filter
    list_filter = ('author',)
    # Search
    search_fields = ("title", )
    # Number of records/fields per page
    list_per_page = 20
    # # radio fields
    # radio_fields = {'author': admin.VERTICAL}
    radio_fields = {'author': admin.HORIZONTAL}
    
    # # Display specific contects
    # def less_content(self, obj):
    #     return obj.content[:30]
    
    # Text color change: we also return html content
    def less_content(self, obj):
        content = obj.content[:30]
        return format_html('<span style="color:red">' + content + '...</span>')
    # HTML code for button
    def click_me(self, obj):
        # open specific blog after button click
        return format_html(f'<a href="/admin/blog/post/{obj.id}" class="button button5">View</a>')

    
    
    
    
    
    
@admin.register(PostComment)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ('sno', 'post', 'author', 'less_comment', 'click_me')
    list_filter = ('post',)
    search_fields = ('post',)
    
    def less_comment(self, obj):
        comment = obj.comment[:30]
        return format_html('<span style="color:red">' + comment + '...</span>')
    
    def click_me(self, obj):
        # open specific blog after button click
        return format_html(f'<a href="/admin/blog/postcomment/{obj.sno}" class="button button5">View</a>')