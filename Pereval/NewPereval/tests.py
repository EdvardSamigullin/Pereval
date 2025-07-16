from django.test import TestCase
from rest_framework.test import APIClient
from .models import User, Pereval
from rest_framework import status


class PerevalAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Создаем пользователя
        self.user = User.objects.create(
            email='qwerty@mail.ru',
            last_name='Петров',
            first_name='Иван',
            middle_name='Николаевич',
            phone='+7 444 44 44'
        )

        self.valid_data = {
            "beauty_title": "пер.",
            "title": "Пр",
            "other_titles": "Тризм",
            "connect": "",
            "add_time": "2021-09-22 13:18:13",
            "user": {
                "email": "qwerty@mail.ru",
                "fam": "Петров",
                "name": "Иван",
                "otc": "Николаевич",
                "phone": "+7 444 44 44"
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
                {"title": "Седловина", "image_url": "http://example.com/image1.jpg"},
                {"title": "Подъем", "image_url": "http://example.com/image2.jpg"}
            ]
        }

    def test_create_and_get_pereval(self):
        # POST запрос для создания перевала с новым пользователем
        response = self.client.post('/api/submitData/', self.valid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 200)  # Выводим статус 200, если создано успешно
        pereval_id = response.data['id']

        # Проверка, что новый пользователь был добавлен в базу данных
        user_email = self.valid_data['user']['email']
        user = User.objects.get(email=user_email)
        self.assertIsNotNone(user)

        # GET запрос по ID
        get_response = self.client.get(f'/api/submitData/{pereval_id}/')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data['title'], self.valid_data['title'])
        self.assertEqual(get_response.data['user']['email'], self.valid_data['user']['email'])

    def test_get_by_email(self):
        # Создаём объект
        self.client.post('/api/submitData/', self.valid_data, format='json')

        # GET по email
        response = self.client.get('/api/submitData/', {'user__email': self.user.email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_patch_pereval(self):
        # Создаем объект
        response = self.client.post('/api/submitData/', self.valid_data, format='json')
        pereval_id = response.data['id']

        # PATCH редактирование данных
        patch_data = {
            "title": "Обновлённый перевал",
            "coords": {
                "latitude": 46.000,
                "longitude": 76.000,
                "height": 1300
            },
            "images": [
                {"title": "Новый вид", "image_url": "http://example.com/new_image.jpg"}
            ]
        }

        patch_response = self.client.patch(f'/api/submitData/{pereval_id}/', patch_data, format='json')
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

        # Проверка обновлений
        updated = self.client.get(f'/api/submitData/{pereval_id}/')
        self.assertEqual(updated.data['title'], patch_data['title'])
        self.assertEqual(updated.data['coords']['height'], patch_data['coords']['height'])
        self.assertEqual(len(updated.data['images']), 1)
        self.assertEqual(updated.data['images'][0]['title'], "Новый вид")

    def test_patch_disallowed_if_status_not_new(self):
        # Создаём объект
        response = self.client.post('/api/submitData/', self.valid_data, format='json')
        pereval_id = response.data['id']

        # Принудительно меняем статус на "accepted"
        pereval = Pereval.objects.get(id=pereval_id)
        pereval.status = 'accepted'
        pereval.save()

        # Пытаемся отправить PATCH
        patch_response = self.client.patch(f'/api/submitData/{pereval_id}/', {"title": "Новое название"}, format='json')
        self.assertEqual(patch_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('state', patch_response.data)
        self.assertEqual(patch_response.data['state'], 0)

    def test_post_with_multiple_images(self):
        # Тест: добавление перевала с несколькими изображениями
        response = self.client.post('/api/submitData/', self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pereval_id = response.data['id']

        get_response = self.client.get(f'/api/submitData/{pereval_id}/')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(get_response.data['images']), 2)
        self.assertEqual(get_response.data['images'][0]['title'], "Седловина")
        self.assertEqual(get_response.data['images'][1]['title'], "Подъем")
