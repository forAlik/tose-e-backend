from django.contrib import admin
from .models import News

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'image_preview', 'content')
    search_fields = ('title', 'slug')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    
    def image_preview(self, obj):
        """این متد برای نمایش پیش‌نمایش تصویر در لیست استفاده می‌شود"""
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50" />'
        return '-'
    image_preview.allow_tags = True

    def content_preview(self, obj):
        return obj.content[:200]
    content_preview.short_description = 'محتوا (چند خط اول)'

admin.site.register(News, NewsAdmin)
