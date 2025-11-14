"""Настройки админки для приложения bookings."""
from django.contrib import admin
from .models import Room, Booking

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Класс настройки отображения модели Room в админке."""
    list_display = ['name', 'capacity', 'has_projector', 'has_whiteboard']
    list_filter = ['has_projector', 'has_whiteboard']
    search_fields = ['name']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Класс настройки отображения модели Booking в админке."""
    list_display = ['room', 'start_time', 'end_time', 'user']
    list_filter = ['room', 'user']
    date_hierarchy = 'start_time'
