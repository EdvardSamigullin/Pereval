"""
Сериализаторы преобразуют данные моделей User, Coords,
Image и Pereval в формат, удобный для API. Сериализаторы обрабатывают
всю необходимую информацию, включая данные пользователя, координаты перевала и изображения.
"""
from .models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'last_name', 'first_name', 'middle_name', 'phone']

    def create(self, validated_data):
        # Пытаемся найти пользователя по email
        user, created = User.objects.get_or_create(
            email=validated_data['email'],
            defaults={
                'last_name': validated_data.get('last_name', ''),
                'first_name': validated_data.get('first_name', ''),
                'middle_name': validated_data.get('middle_name', ''),
                'phone': validated_data.get('phone', ''),
            }
        )
        return user

class CoordsSerializer(serializers.ModelSerializer):
   class Meta:
       model = Coords
       fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['title', 'image_url'] # # Здесь image_url будет хранить ссылку на изображения


class PerevalSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    images = ImageSerializer(many=True)

    class Meta:
        model = Pereval
        fields = [
            'beauty_title', 'title', 'other_titles', 'connect', 'add_time',
            'user', 'coords',
            'level_winter', 'level_summer', 'level_autumn', 'level_spring',
            'images'
        ]

    def create(self, validated_data):
        # Извлекаем вложенные данные
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        images_data = validated_data.pop('images')

        # # Создаём или находим пользователя
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        # Создаем координаты
        coords = Coords.objects.create(**coords_data)

        # Создаем сам перевал
        pereval = Pereval.objects.create(user=user, coords=coords, **validated_data)

        # Создаем изображения и связываем их с перевалом
        for image_data in images_data:
            Image.objects.create(pereval=pereval, **image_data)

        return pereval

class InfoSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    images = ImageSerializer(many=True)

    class Meta:
        model = Pereval
        fields = [
            'beauty_title', 'title', 'other_titles', 'connect', 'add_time',
            'status', 'user', 'coords',
            'level_winter', 'level_summer', 'level_autumn', 'level_spring',
            'images'
        ]