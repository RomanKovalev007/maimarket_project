from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from users.models import User
from goods.models import Goods, Categories, Condition, Address
from ..models import Favorites
import tempfile
import shutil



MEDIA_ROOT = tempfile.mkdtemp()

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class FavoritesIntegrationTest(TestCase):
    @classmethod
    def tearDownClass(cls):
        """Удаляем временную папку с медиафайлами после всех тестов"""
        super().tearDownClass()
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        
    def setUp(self):
        self.client = Client()
        test_image = SimpleUploadedFile(
            name='test.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00',
            content_type='image/jpeg'
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Categories.objects.create(
            name='Electronics'
        )
        self.address = Address.objects.create(
            name='Test address',
            address='test address',
            link_to_map='#'
        )
        self.condition = Condition.objects.create(
            name='Test condition'
        )

        self.product = Goods.objects.create(
            name='Smartphone',
            price=1000,
            seller=self.user,
            is_published=True,
            category=self.category,
            condition=self.condition,
            address=self.address,
            image=test_image

        )

        self.client.login(username='testuser', password='testpass123')

    def test_full_favorite_flow(self):
        # 1. Добавляем в избранное через API
        response = self.client.post(
            reverse('favorites:change', kwargs={'ad_id': self.product.id}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Favorites.objects.filter(user=self.user, product=self.product).exists())

        # 2. Проверяем список избранного
        response = self.client.get(reverse('favorites:fav_list'))
        self.assertContains(response, 'Smartphone')

        # 3. Удаляем из избранного
        response = self.client.post(
            reverse('favorites:change', kwargs={'ad_id': self.product.id}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Favorites.objects.filter(user=self.user, product=self.product).exists())