"""
Представления реализуют REST API для добавления, получения и редактирования перевалов
с использованием APIView и документации через drf_yasg.

Классы:

- SubmitData:
    - GET: Возвращает список перевалов по email (`user__email`). Если не указан — ошибка 400.
    - POST: Добавляет новый перевал с вложенными данными (user, coords, images).
      При успехе — статус 201 и id. Обработка — через `handle_valid_data` / `handle_invalid_data`.

- PerevalRetrieveUpdateView:
    - GET: Возвращает данные перевала по ID. При успехе — статус 200, иначе 404.
    - PATCH: Обновляет перевал по ID, если статус = "new". Обновляются поля, координаты, изображения.
      При успехе — `state: 1`, иначе — `state: 0`.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PerevalSerializer, InfoSerializer,  PerevalUpdateSerializer
from .models import Pereval
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class SubmitData(APIView):
    # Описание GET-запроса для получения перевалов по email
    @swagger_auto_schema(
        operation_description="Получить список перевалов по email пользователя",
        manual_parameters=[
            openapi.Parameter(
                'user__email',
                openapi.IN_QUERY,
                description="Email пользователя, чьи перевалы нужно получить",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={200: InfoSerializer(many=True)}
    )
    # Получаем перевалы, связанные email
    def get(self, request):
        email = request.query_params.get('user__email')
        if not email:
            return Response({'error': 'Не указан параметр user__email'}, status=400)

        perevals = Pereval.objects.filter(user__email=email)
        serializer = InfoSerializer(perevals, many=True)
        return Response(serializer.data, status=200)

    # Описание POST-запроса на добавление перевала
    @swagger_auto_schema(
        operation_description="Отправить новый перевал",
        request_body=PerevalSerializer,
        responses={201: openapi.Response(description="Успешное создание", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_INTEGER),
                'message': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                'id': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ))}
    )
    # Добавление перевала в БД
    def post(self, request):
        serializer = PerevalSerializer(data=request.data)
        if serializer.is_valid():
            return self.handle_valid_data(serializer)
        return self.handle_invalid_data(serializer)

    def handle_valid_data(self, serializer):
        try:
            # Сохранение перевала, если данные валидны
            pereval = serializer.save()
            return Response({
                'status': 200,
                'message': None,
                'id': pereval.id
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'status': 500,
                'message': f'Ошибка при сохранении: {str(e)}',
                'id': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def handle_invalid_data(self, serializer):
        # Возвращаем ошибку, если данные невалидны
        return Response({
            'status': 400,
            'message': 'Ошибка валидации',
            'errors': serializer.errors,
            'id': None
        }, status=status.HTTP_400_BAD_REQUEST)

class PerevalRetrieveUpdateView(APIView):
    # Описание GET-запроса на получение информации о перевале по ID
    @swagger_auto_schema(
        operation_description="Получить подробную информацию о перевале по ID",
        responses={200: InfoSerializer()}
    )

    # Получение информации о перевале по ID
    def get(self, request, id):
        pereval = get_object_or_404(Pereval, id=id)
        serializer = InfoSerializer(pereval)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Описание PATCH-запроса на частичное обновление перевала
    @swagger_auto_schema(
        operation_description="Обновить перевал по ID (если статус = 'new')",
        request_body=PerevalUpdateSerializer,
        responses={
            200: openapi.Response(description="Успешное обновление", schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'state': openapi.Schema(type=openapi.TYPE_INTEGER)}
            )),
            400: "Ошибка валидации или статус не 'new'"
        }
    )

    # Обновление перевала
    def patch(self, request, id):
        # Получаем объект перевала по ID
        pereval = get_object_or_404(Pereval, id=id)

        if pereval.status != 'new':
            return Response({
                'state': 0,
                'message': 'Запись не может быть отредактирована, так как ее статус не "new".'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Проводим частичное обновление
        serializer = PerevalUpdateSerializer(pereval, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'state': 1}, status=status.HTTP_200_OK)
        # В случае ошибок валидации
        return Response({'state': 0, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
