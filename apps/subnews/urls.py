from django.urls import path
from .views import SubnewsAPIView, SubnewsDetailAPIView

app_name = 'subnews'

urlpatterns = [
    path('', SubnewsAPIView.as_view(), name='subnews-list'),  # GET_ALL + POST
    path('<int:pk>/', SubnewsDetailAPIView.as_view(), name='subnews-detail'),  # GET/PUT/PATCH/DELETE
]