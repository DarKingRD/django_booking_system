"""Представления (ViewSets) для API системы бронирования переговорных комнат.

Содержит:
- RoomViewSet: только для чтения информации о доступных комнатах;
- BookingViewSet: для создания, просмотра и удаления собственных бронирований
  с автоматической привязкой к авторизованному пользователю.
"""
from rest_framework import viewsets
from bookings.models import Room, Booking
from .serializers import RoomSerializer, BookingSerializer


class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для просмотра переговорных комнат.

    Поддерживает только операции чтения:
    - GET /rooms/ — список всех комнат,
    - GET /rooms/<id>/ — детальная информация о комнате.

    Не позволяет создавать, изменять или удалять комнаты через API.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """Представление для управления бронированиями пользователя.

    Поддерживает:
    - POST /bookings/ — создание нового бронирования,
    - GET /bookings/ — список бронирований текущего пользователя,
    - DELETE /bookings/<id>/ — удаление собственного бронирования.

    Пользователь не имеет доступа к бронированиям других пользователей.
    """
    serializer_class = BookingSerializer

    def get_queryset(self):
        """Возвращает только бронирования текущего пользователя."""
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Сохраняет бронирование, автоматически устанавливая владельца."""
        serializer.save(user=self.request.user)
