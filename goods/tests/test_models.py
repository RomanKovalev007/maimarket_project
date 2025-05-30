from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from goods.models import Categories, Address, Condition, Goods
from users.models import User
import os
from django.conf import settings
import tempfile
import shutil


MEDIA_ROOT = tempfile.mkdtemp()

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class GoodsModelsTest(TestCase):
    @classmethod
    def tearDownClass(cls):
        """Удаляем временную папку с медиафайлами после всех тестов"""
        super().tearDownClass()
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Categories.objects.create(
            name='Electronics',
            slug='electronics'
        )
        self.address = Address.objects.create(
            name='Moscow',
            slug='moscow',
            address='Red Square',
            link_to_map='https://maps.example.com'
        )
        self.condition = Condition.objects.create(
            name='New',
            slug='new'
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Electronics')
        self.assertEqual(str(self.category), 'Electronics')

    def test_address_creation(self):
        self.assertEqual(self.address.name, 'Moscow')
        self.assertEqual(self.address.address, 'Red Square')
        self.assertEqual(str(self.address), 'Moscow')

    def test_goods_creation(self):
        test_image = SimpleUploadedFile(
            name='test.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00',
            content_type='image/jpeg'
        )
        goods = Goods.objects.create(
            name='Smartphone',
            slug='smartphone',
            description='Test description',
            image=test_image,
            price=1000,
            category=self.category,
            seller=self.user,
            condition=self.condition,
            address=self.address
        )

        self.assertEqual(goods.name, 'Smartphone')
        self.assertEqual(goods.price, 1000)
        self.assertTrue(goods.is_published)
        self.assertEqual(goods.seller.username, 'testuser')

        # Проверка автоматического создания slug
        self.assertEqual(goods.slug, 'smartphone')

        # Проверка загрузки изображения
        self.assertTrue(os.path.exists(os.path.join(settings.MEDIA_ROOT, goods.image.path)))
        os.remove(goods.image.path)  # Очистка

        # Проверка get_absolute_url
        self.assertEqual(goods.get_absolute_url(), '/goods/ad/smartphone/')