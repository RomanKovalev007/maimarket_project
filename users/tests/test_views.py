from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model

from goods.models import Goods, Categories, Address, Condition
import tempfile
import shutil


User = get_user_model()


MEDIA_ROOT = tempfile.mkdtemp()

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ViewsTest(TestCase):
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

    def test_login_view(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_register_view(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_profile_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:profile', kwargs={'user_id': self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_unpublished_goods_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:profile_not_published'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_edit_profile_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:profile_change_data'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/edit_profile.html')