from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('about/', views.about),
    path('login/', views.custom_login),
    path('logout/', views.custom_logout),
]