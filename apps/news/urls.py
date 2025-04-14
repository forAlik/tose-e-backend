from django.urls import path
from .views import NewsAPIView

app_name = 'news'

urlpatterns = [
    path('', NewsAPIView.as_view(), name='news-list'),
    path('<int:pk>/', NewsAPIView.as_view(), name='news-detail'),
    path('<str:slug>/', NewsAPIView.as_view(), name='news-detail'),
]
