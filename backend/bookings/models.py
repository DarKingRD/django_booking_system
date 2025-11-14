"""Модели для приложения bookings.

Содержит две основные модели:
- Room: описывает переговорную комнату с техническими характеристиками;
- Booking: представляет бронирование комнаты конкретным пользователем
  на заданный временной интервал.
"""
from django.db import models
from django.contrib.auth import get_user_model

# Получаем модель пользователя из настроек Django
User = get_user_model()

class Room(models.Model):
    """Представляет переговорную комнату в университете.

    Содержит информацию о вместимости и доступном оборудовании,
    необходимую для принятия решения о бронировании.
    """
    name = models.CharField(
        max_length=100,
        verbose_name="Название комнаты",
        help_text="Например: «Комната 305» или «Большой конференц-зал»"
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Подробное описание комнаты"
    )
    capacity = models.PositiveIntegerField(
        verbose_name="Вместимость",
        help_text="Количество человек, которое может поместиться в комнату"
    )
    has_projector = models.BooleanField(
        default=False,
        verbose_name="Наличие проектора",
        help_text="Указывает, есть ли проектор в комнате"
    )
    has_whiteboard = models.BooleanField(
        default=False,
        verbose_name="Наличие доски",
        help_text="Указывает, есть ли доска в комнате"
    )

    def __str__(self):
        return f"{self.name}"

class Booking(models.Model):
    """Бронирование переговорной комнаты на определённое время.

    Привязано к пользователю и комнате. Гарантирует, что один и тот же
    временной слот не может быть забронирован дважды (логика валидации
    реализуется на уровне API или бизнес-логики).
    """
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        verbose_name="Комната",
        related_name="bookings",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="bookings",
        )
    start_time = models.DateTimeField(
        verbose_name="Начало бронирования",
    )
    end_time = models.DateTimeField(
        verbose_name="Окончание бронирования"
    )

    def __str__(self):
        return f"{self.room.name} - {self.start_time} - {self.end_time}"

    class Meta:
        """
        Метаданные для модели Booking.
        """
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ["start_time"]
