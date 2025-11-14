"""
    Здесь представлены модели для приложения bookings
"""
from django.db import models

# Create your models here.
class Room(models.Model):
    """
    Модель для комнат
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    capacity = models.PositiveIntegerField()
    has_projector = models.BooleanField(default=False)
    has_whiteboard = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

class Booking(models.Model):
    """
    Модель для бронирования
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.room.name} - {self.start_time} - {self.end_time}"
