"""Маршруты API для приложения bookings."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, BookingViewSet, register

router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('register/', register, name='register'),
    path('', include(router.urls)),  # Основные маршруты (rooms, bookings)
]
