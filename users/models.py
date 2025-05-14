from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True, null=True, verbose_name="Фотография")
    number = models.PositiveBigIntegerField(blank=True, null=True, verbose_name='Контактный телефон')
    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'user_id': self.id})