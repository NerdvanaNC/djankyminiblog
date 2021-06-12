from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main),
    path('about/', views.about),
    path('register/', views.custom_register),
    path('logout/', views.custom_logout),
    path('tinymce/', include('tinymce.urls')),
    path('like/', views.ajax_like),
    path('unlike/', views.ajax_unlike),
]