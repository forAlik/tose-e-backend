from django.urls import path
from .views import AchievementsAPIView, AchievementsDetailAPIView

app_name = 'achievements'

urlpatterns = [
    path('', AchievementsAPIView.as_view(), name='achievements-list'),
    path('<int:pk>/', AchievementsDetailAPIView.as_view(), name='achievements-detail'),
]