from django import forms
from django.contrib import admin
from .models import News

class NewsAdminForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),  # استفاده از textarea ساده
        }

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    readonly_fields = ('content_html',)  # نمایش نسخه HTML
    
    # تنظیم فیلدهای قابل نمایش
    list_display = ('title', 'content_preview')
    
    def content_preview(self, obj):
        return obj.content_html[:100] + "..." if obj.content_html else ""
    content_preview.short_description = "پیش نمایش محتوا"