from django.urls import path
from .views import NewsAPIView

app_name = 'news'

urlpatterns = [
    path('', NewsAPIView.as_view(), name='news-list'),  # برای ایجاد یا گرفتن همه اخبار
    path('<int:pk>/', NewsAPIView.as_view(), name='news-detail'),  # برای گرفتن، ویرایش و حذف خبر خاص
]
