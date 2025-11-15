"""Сериализаторы для API системы бронирования переговорных комнат.

Содержит сериализаторы:
- RoomSerializer — для отображения информации о комнатах;
- BookingSerializer — для создания и управления бронированиями,
  включая валидацию временных интервалов и автоматическую привязку
  к текущему пользователю.
"""
from rest_framework import serializers
from bookings.models import Room, Booking
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
class RoomSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Room.
    
    Предназначен для преобразования данных переговорных комнат
    (название, вместимость, наличие оборудования) в формат JSON и обратно.
    Используется в API для получения списка комнат и детальной информации.
    """
    class Meta:
        """
        Docstring для Meta
        """
        model = Room
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Booking.

    Обрабатывает создание и отображение бронирований переговорных комнат.
    Поле 'user' устанавливается автоматически на основе авторизованного пользователя
    и недоступно для редактирования через API.
    Включает валидацию временных интервалов бронирования.
    """
    class Meta:
        """Метаданные сериализатора BookingSerializer."""
        model = Booking
        fields = '__all__'
        read_only_fields = ['user']

    def validate(self, data):
        """Выполняет кастомную валидацию временных границ бронирования.

        Проверяет, что:
        - время начала брони строго меньше времени окончания;
        - время начала не находится в прошлом (с учётом временной зоны);
        - в выбранной комнате нет пересекающихся бронирований.

        Args:
            data (dict): Данные, прошедшие первичную валидацию DRF.

        Returns:
            dict: Проверенные и, при необходимости, модифицированные данные.

        Raises:
            serializers.ValidationError: Если временные ограничения нарушены.
        """
        start = data.get('start_time')
        end = data.get('end_time')

        if start and end:
            if start >= end:
                raise serializers.ValidationError(
                    "Время начала бронирования должно быть раньше времени окончания."
                )
            if start < timezone.now():
                raise serializers.ValidationError(
                    "Нельзя создать бронирование на прошедшее время."
                )

        room = data.get('room')
        if room and start and end:
            conflicting_bookings = Booking.objects.filter(
                room=room,
                start_time__lt=end,
                end_time__gt=start
            )
            if self.instance:
                conflicting_bookings = conflicting_bookings.exclude(id=self.instance.id)

            if conflicting_bookings.exists():
                raise serializers.ValidationError(
                    "Эта комната уже занята в выбранное время"
                )

        return data
