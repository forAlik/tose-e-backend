from rest_framework import serializers
from .models import News
from PIL import Image
import imghdr
from django.core.exceptions import ValidationError

class NewsSerializer(serializers.ModelSerializer):
    jalali_created_at = serializers.SerializerMethodField()
    
    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'image', 'created_at', 'jalali_created_at']
        extra_kwargs = {
            'created_at': {'read_only': True}
        }

    def get_jalali_created_at(self, obj):
        return obj.get_jalali_created_at()

    def validate_image(self, value):
        if value:
            if not value.name.lower().endswith('.webp'):
                raise ValidationError("فقط فایل‌های با فرمت WebP قابل قبول هستند")
            
            if value.size > 4 * 1024 * 1024:
                raise ValidationError("حجم تصویر باید کمتر از 2MB باشد")
            
            try:
                img = Image.open(value)
                width, height = img.size
                
                if width != 600 or height != 400:
                    raise ValidationError(
                        f"اندازه تصویر باید دقیقاً 600x400 پیکسل باشد. (تصویر آپلود شده {width}x{height} است)"
                    )
                    
                value.seek(0)
                if imghdr.what(value) != 'webp':
                    raise ValidationError("فایل بارگذاری شده یک تصویر WebP معتبر نیست")
                    
            except Exception as e:
                raise ValidationError(f"خطا در پردازش تصویر: {str(e)}")
            finally:
                value.seek(0)
            
        return value
    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("عنوان خبر باید حداقل 10 کاراکتر باشد")
        return value