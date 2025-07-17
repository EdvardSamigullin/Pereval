# Проект бэкенда для работы приложения базы горных перевалов.
## (практика Skillfactory) ##

## Описание проекта

REST API для приёма и хранения информации о перевалах в рамках проекта ФСТР (Федерация спортивного туризма России).  
Сервис предоставляет возможность:

- Отправлять информацию о перевале (`POST`)
- Получать список перевалов по email пользователя (`GET`)
- Получать подробную информацию о перевале по его ID (`GET`)
- Обновлять данные перевала, если его статус — `"new"` (`PATCH`)

Документация автоматически доступна через Swagger и ReDoc.

## Структура проекта

- `submitData/PerevalBase/pereval/models.py` — модели пользователя, перевала, координат и изображений  
- `submitData/PerevalBase/pereval/serializers.py` — сериализаторы для POST/GET/PATCH  
- `submitData/PerevalBase/pereval/views.py` — реализация логики API  
- `submitData/PerevalBase/pereval/urls.py` — маршруты приложения  
- `submitData/PerevalBase/PerevalBase/settings.py` — настройки проекта с подключением .env  
- `submitData/PerevalBase/PerevalBase/urls.py` — главные маршруты проекта  

## Пример POST-запроса

```json
{
    "beauty_title": "пер. ",
    "title": "Пхия",
    "other_titles": "Триев",
    "connect": "",
    "add_time": "2021-09-22 13:18:13",
    "user": {
        "email": "qwerty@mail.ru",
        "last_name": "Пупкин",
        "first_name": "Василий",
        "middle_name": "Иванович",
        "phone": "+7 555 55 55"
    },
    "coords": {
        "latitude": "45.3842",
        "longitude": "7.1525",
        "height": "1200"
    },
    "level": {
        "winter": "",
        "summer": "1А",
        "autumn": "1А",
        "spring": ""
    },
    "images": [
        {"file_path": "седловина.jpg", "title": "Седловина"},
        {"file_path": "подъем.jpg", "title": "Подъём"}
    ]
}

```

##  Ответ:

```json
{
  "status": 200,
  "message": null,
  "id": 42
}
```
## Установка


 1. Клонировать репозиторий
git clone https://github.com/EdvardSamigullin/Pereval.git

2. Установить необходимые библиотеки

 3. Запустить сервер
python manage.py runserver

## Документация API

После запуска проекта, API-документация доступна по адресам:

- Swagger UI: http://localhost:8000/swagger/  
- ReDoc: http://localhost:8000/redoc/


## Доступные эндпоинты: 
_POST `/api/submitData/`  - создаёт объект "перевал"\
_PATCH `/api/submitData/<id>/` - редактирует объект "перевал"\
_GET  `/api/submitData/<id>/`- извлекает информацию об объекте "перевал"\
_GET  `/api/submitData/?user__email=example@mail.ru` - извлекает список объектов созданных одним пользователем 

___

##  Ограничения

- Перевал можно редактировать только если его статус — `"new"`.
- Для создания перевала требуется, чтобы пользователь с указанным email уже существовал или был создан вместе с перевалом.

