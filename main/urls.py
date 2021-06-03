from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('about/', views.about),
    path('register/', views.custom_register),
    path('logout/', views.custom_logout),
]