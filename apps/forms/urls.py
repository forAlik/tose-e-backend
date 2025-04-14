from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('create/', views.create_form),
    path('', views.get_forms),
]