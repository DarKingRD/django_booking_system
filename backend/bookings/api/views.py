"""Представления (ViewSets) для API системы бронирования переговорных комнат.

Содержит:
- RoomViewSet: только для чтения информации о доступных комнатах;
- BookingViewSet: для создания, просмотра и удаления собственных бронирований
  с автоматической привязкой к авторизованному пользователю.
"""
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from bookings.models import Room, Booking
from .serializers import (
    RoomSerializer, BookingSerializer, UserRegistationSerializer
)
from drf_spectacular.utils import extend_schema

@extend_schema(
    request=UserRegistationSerializer,
    responses={201: {"type": "object", "properties": {"message": {"type": "string"}}}},
    description="Регистрация нового пользователя. Принимает username, email и password."
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Регистрация нового пользователя."""
    serializer = UserRegistationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Пользователь успешно зарегестрирован"},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP400_BAD_REQUEST)

class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для просмотра переговорных комнат.

    Поддерживает только операции чтения:
    - GET /rooms/ — список всех комнат,
    - GET /rooms/<id>/ — детальная информация о комнате.

    Не позволяет создавать, изменять или удалять комнаты через API.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]


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
