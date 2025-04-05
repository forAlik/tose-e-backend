from django.urls import path
from .views import NewsAPIView, NewsDetailAPIView

app_name = 'news'

urlpatterns = [
    path('', NewsAPIView.as_view(), name='news-list'),
    path('<int:pk>/', NewsDetailAPIView.as_view(), name='news-detail'),
]