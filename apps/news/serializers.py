from rest_framework import serializers
from .models import News
import jdatetime
from datetime import timedelta
class NewsSerializer(serializers.ModelSerializer):
    created_at_jalali = serializers.SerializerMethodField()
    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'created_at', 'created_at_jalali', 'image', 'slug']

    def get_created_at_jalali(self, obj):
        if obj.created_at:
            date = obj.created_at

            jdate = jdatetime.datetime.fromgregorian(datetime=date)

            tehran_time = jdate + timedelta(hours=3, minutes=30)

            return tehran_time.strftime('%H:%M - %Y/%m/%d ')
        return None