from io import BytesIO

from PIL import Image
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from goods.models import Goods, Categories, Address, Condition
from users.models import User
import tempfile
import shutil


MEDIA_ROOT = tempfile.mkdtemp()

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class GoodsIntegrationTest(TestCase):
    @classmethod
    def tearDownClass(cls):
        """Удаляем временную папку с медиафайлами после всех тестов"""
        super().tearDownClass()
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Categories.objects.create(name='Electronics')
        self.address = Address.objects.create(
            name='Moscow',
            address='Red Square',
            link_to_map='https://maps.example.com'
        )
        self.condition = Condition.objects.create(name='New')
        self.client.login(username='testuser', password='testpass123')
    def create_test_image(self):
        # Создаем простое изображение 100x100 пикселей
        image = Image.new('RGB', (100, 100), color='red')
        image_io = BytesIO()
        image.save(image_io, format='JPEG', quality=100)
        image_io.seek(0)
        return SimpleUploadedFile(
            name='test.jpg',
            content=image_io.getvalue(),
            content_type='image/jpeg'
        )

    def test_full_ad_lifecycle(self):
        # 1. Добавление товара

        response = self.client.post(reverse('goods:add_ad'), {
            'name': 'New Product',
            'category': self.category.id,
            'address': self.address.id,
            'condition': self.condition.id,
            'description': 'Test description',
            'price': 1000,
            'image': self.create_test_image()
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Goods.objects.filter(name='New Product').exists())

        goods = Goods.objects.get(name='New Product')

        # 2. Просмотр товара
        response = self.client.get(reverse('goods:ad', kwargs={'ad_slug': goods.slug}))
        self.assertContains(response, 'Test description')

        # 3. Редактирование товара
        response = self.client.post(reverse('goods:edit', kwargs={'ad_slug': goods.slug}), {
            'name': 'Updated Product',
            'category': self.category.id,
            'address': self.address.id,
            'condition': self.condition.id,
            'description': 'Updated description',
            'price': 1200
        }, follow=True)

        self.assertContains(response, 'Updated Product')
        goods.refresh_from_db()
        self.assertEqual(goods.price, 1200)

        # 4. Снятие с публикации
        response = self.client.get(reverse('goods:publish', kwargs={'ad_slug': goods.slug}),
                                   HTTP_REFERER=reverse('goods:ad', kwargs={'ad_slug': goods.slug}))
        goods.refresh_from_db()
        self.assertFalse(goods.is_published)