"""
Модели для REST API проекта ФСТР (Федерация спортивного туризма России).

1. User — модель пользователя. Идентификация осуществляется по уникальному email.
   Содержит ФИО и номер телефона.
2. Coords — модель координат перевала. Содержит широту, долготу и высоту.
3. Image — модель изображения перевала. Хранит заголовок и URL изображения,
   связана с перевалом.
4. Pereval — основная модель для хранения информации о перевале:
   - Названия, дата добавления, описание соединяемых точек.
   - Связь с пользователем, координатами, изображениями.
   - Уровни сложности по сезонам: зима, лето, осень, весна.
   - Статус модерации: новая, на проверке, принята или отклонена.

Уровни сложности и статусы задаются с помощью `choices`, что обеспечивает контроль вводимых
данных.
Модель Image связана с Pereval через ForeignKey (один ко многим),
а координаты — через OneToOne (один к одному).
"""

from django.db import models
from django.utils import timezone
# Create your models here.
class User(models.Model):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20,blank=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.email})"


class Coords(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    height = models.IntegerField()
    def __str__(self):
        return f"Широта: {self.latitude}, Долгота: {self.longitude}, Высота: {self.height}"

class Pereval(models.Model):
    beauty_title = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    other_titles = models.CharField(max_length=255, blank=True)
    connect = models.TextField(blank=True)
    add_time = models.DateTimeField(default=timezone.now)
    level_winter = models.CharField(max_length=3, blank=True)
    level_summer = models.CharField(max_length=3, blank=True)
    level_autumn = models.CharField(max_length=3, blank=True)
    level_spring = models.CharField(max_length=3, blank=True)

    # Статус модерации
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('pending', 'На модерации'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')

    # Связи
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='perevals')
    coords = models.OneToOneField(Coords, on_delete=models.CASCADE, related_name='pereval')

    def __str__(self):
        return f"{self.beauty_title} {self.title} ({self.add_time.strftime('%Y-%m-%d')})"

class Image(models.Model):
    pereval = models.ForeignKey('Pereval', on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=100)
    image_url = models.URLField()  # хранится ссылка на изображение
    def __str__(self):
        return f"{self.title} - {self.image_url}"