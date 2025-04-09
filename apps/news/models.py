from django.db import models
from jalali_date import date2jalali
from django.utils import timezone
from django_quill.fields import QuillField
class News(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان")
    content = QuillField(verbose_name="محتوا")
    image = models.ImageField(upload_to='news_images/', null=True, blank=True, verbose_name="تصویر")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True, default="temp-slug")
    def __str__(self):
        
        return self.title
    
    def get_jalali_created_at(self):
        return date2jalali(self.created_at).strftime('%Y/%m/%d - %H:%M')
    
    class Meta:
        verbose_name = 'خبر'
        verbose_name_plural = 'اخبار'