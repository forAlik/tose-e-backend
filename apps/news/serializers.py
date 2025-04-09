from rest_framework import serializers
from .models import News
from django.core.exceptions import ValidationError
from django_quill.quill import QuillParseError
from PIL import Image

class NewsSerializer(serializers.ModelSerializer):
    content_html = serializers.ReadOnlyField()
    get_jalali_created_at = serializers.ReadOnlyField()

    class Meta:
        model = News
        fields = [
            'id',
            'title',
            'content',
            'content_html',
            'image',
            'created_at',
            'get_jalali_created_at',
            'slug',
        ]

    def validate_image(self, image):
        if not image.name.endswith('.webp'):
            raise serializers.ValidationError("فقط فرمت WEBP قابل قبول است.")

        if image.size > 4 * 1024 * 1024:
            raise serializers.ValidationError("حجم تصویر نباید بیشتر از ۴ مگابایت باشد.")

        try:
            img = Image.open(image)
            if img.width != 600 or img.height != 400:
                raise serializers.ValidationError("ابعاد تصویر باید دقیقاً 600x400 پیکسل باشد.")
        except Exception:
            raise serializers.ValidationError("خواندن تصویر با مشکل مواجه شد.")

        return image

    def validate_content(self, content):
        if not content:
            raise serializers.ValidationError("محتوا نمی‌تواند خالی باشد.")      
        try:
            str(content)
        except QuillParseError:
            raise serializers.ValidationError("محتوا به درستی قابل parse نیست.")
        
        return content
