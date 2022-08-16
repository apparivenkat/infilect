from django.urls import path, include   
from .views import LoginAPIView, RegisterAPIView, Weather, logout_view

urlpatterns = [
    path('register', RegisterAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('logout', logout_view, name='logout'),
    path('weather', Weather.as_view(), name='weather'),
]
