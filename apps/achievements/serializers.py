from rest_framework import serializers
from .models import Achievements
from PIL import Image
from django.core.exceptions import ValidationError
import imghdr

class AchievementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievements
        fields = ['id', 'title', 'image']
        extra_kwargs = {
            'image': {
                'required': False,
                'error_messages': {
                    'invalid_image': 'فقط فرمت WebP قابل قبول است'
                }
            }
        }

    def validate_image(self, value):
        if value:
            if not value.name.lower().endswith('.webp'):
                raise ValidationError("فقط فایل‌های با فرمت WebP قابل قبول هستند")
            
            if value.size > 4 * 1024 * 1024:
                raise ValidationError("حجم تصویر باید کمتر از 2MB باشد")
            
            try:
                img = Image.open(value)
                width, height = img.size
                
                if width != 700 or height != 900:
                    raise ValidationError(
                        f"اندازه تصویر باید دقیقاً 700x900 پیکسل باشد. (تصویر آپلود شده {width}x{height} است)"
                    )
                    
                value.seek(0)
                if imghdr.what(value) != 'webp':
                    raise ValidationError("فایل بارگذاری شده یک تصویر WebP معتبر نیست")
                    
            except Exception as e:
                raise ValidationError(f"خطا در پردازش تصویر: {str(e)}")
            finally:
                value.seek(0)
            
        return value