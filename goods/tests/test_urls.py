from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from goods.models import Goods, Categories, Address, Condition
from users.models import User
import tempfile
import shutil


MEDIA_ROOT = tempfile.mkdtemp()

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class GoodsUrlsTest(TestCase):
    @classmethod
    def tearDownClass(cls):
        """Удаляем временную папку с медиафайлами после всех тестов"""
        super().tearDownClass()
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        test_image = SimpleUploadedFile(
            name='test.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00',
            content_type='image/jpeg'
        )
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Categories.objects.create(
            name='Test Category'
        )
        self.address = Address.objects.create(
            name='Test address',
            address='test address',
            link_to_map='#'
        )
        self.condition = Condition.objects.create(
            name='Test condition'
        )

        self.goods = Goods.objects.create(
            name='Test Product',
            price=100,
            seller=self.user,
            is_published=True,
            category=self.category,
            condition=self.condition,
            address=self.address,
            image=test_image

        )

    def test_goods_list_url(self):
        response = self.client.get(reverse('goods:goods_list'))
        self.assertEqual(response.status_code, 200)

    def test_show_ad_url(self):
        response = self.client.get(reverse('goods:ad', kwargs={'ad_slug': 'test-product'}))
        self.assertEqual(response.status_code, 200)

    def test_add_ad_url_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('goods:add_ad'))
        self.assertEqual(response.status_code, 200)

    def test_edit_ad_url(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('goods:edit', kwargs={'ad_slug': 'test-product'}))
        self.assertEqual(response.status_code, 200)