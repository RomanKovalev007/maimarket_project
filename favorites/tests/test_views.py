from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from goods.models import Goods, Categories, Address, Condition
from favorites.models import Favorites
import json
import tempfile
import shutil



MEDIA_ROOT = tempfile.mkdtemp()
User = get_user_model()

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class FavoritesViewsTest(TestCase):
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

    def test_fav_list_view(self):
        Favorites.objects.create(user=self.user, product=self.product)
        response = self.client.get(reverse('favorites:fav_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Smartphone')

    def test_fav_change_add(self):
        response = self.client.post(
            reverse('favorites:change', kwargs={'ad_id': self.product.id}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['is_favorite'])
        self.assertTrue(Favorites.objects.filter(user=self.user, product=self.product).exists())

    def test_fav_change_remove(self):
        Favorites.objects.create(user=self.user, product=self.product)
        response = self.client.post(
            reverse('favorites:change', kwargs={'ad_id': self.product.id}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['is_favorite'])
        self.assertFalse(Favorites.objects.filter(user=self.user, product=self.product).exists())

    def test_fav_change_unauthenticated(self):
        self.client.logout()
        response = self.client.post(
            reverse('favorites:change', kwargs={'ad_id': self.product.id}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login