from django.urls import path
from .views import UserAPIView, UserDetailAPIView, LoginAPI, LogoutAPI

app_name = 'users'

urlpatterns = [
    path('', UserAPIView.as_view(), name='user-list'),  # GET_ALL + POST
    path('<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),  # GET/PUT/PATCH/DELETE
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
]