from django.contrib import admin
from .models import Forms

class FormsAdmin(admin.ModelAdmin):
        list_display = ('fullname', 'subject', 'phone', 'email', 'message')  # فیلدهایی که در لیست نمایش داده می‌شوند
        search_fields = ('fullname', 'phone')  # قابلیت جستجو بر اساس عنوان و اسلاگ
        list_filter = ('created_at',)  # قابلیت فیلتر کردن بر اساس تاریخ ایجاد
        ordering = ('-created_at',)  # مرتب‌سازی بر اساس تاریخ ایجاد به صورت نزولی

admin.site.register(Forms, FormsAdmin)