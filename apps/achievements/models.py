from django.db import models
from django.core.validators import FileExtensionValidator

class Achievements(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان")
    image = models.ImageField(
        upload_to='achievements/',
        null=True,
        blank=True,
        verbose_name="تصویر",
        validators=[FileExtensionValidator(allowed_extensions=['webp'])],
        help_text="فقط فایل‌های WebP با ابعاد 700x900 پیکسل قابل قبول هستند"
    )

    def save(self, *args, **kwargs):
        if self.image:
            if not self.image.name.lower().endswith('.webp'):
                raise ValueError("فقط فرمت WebP قابل قبول است")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دستاورد'
        verbose_name_plural = 'دستاوردها'