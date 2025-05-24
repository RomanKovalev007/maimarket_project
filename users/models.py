from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import uuid
import os

def upload_to(instance, filename):
    # Получаем текущую дату
    now = datetime.now()
    year = now.strftime('%Y')
    month = now.strftime('%m')
    day = now.strftime('%d')

    # Генерируем уникальное имя файла
    ext = filename.split('.')[-1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"

    # Если нужно использовать название товара
    if hasattr(instance, 'name') and instance.name:
        base_name = slugify(instance.name)[:50]  # Ограничиваем длину
        unique_name = f"{base_name}_{unique_name}"

    # Формируем путь: media/users/год/месяц/день/файл
    return os.path.join('users', year, month, day, unique_name)

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    photo = models.ImageField(upload_to=upload_to, blank=True, null=True, verbose_name="Фотография")
    number = models.PositiveBigIntegerField(blank=True, null=True, verbose_name='Контактный телефон')
    telegram = models.SlugField(null=True, blank=True, verbose_name='Ссылка на телеграмм')

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'user_id': self.id})
