from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from favorites.models import Favorites
from goods.models import Goods, Categories, Address, Condition
from users.models import User
import tempfile
import shutil



MEDIA_ROOT = tempfile.mkdtemp()

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class FavoritesModelTest(TestCase):
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


    def test_favorite_creation(self):
        favorite = Favorites.objects.create(
            user=self.user,
            product=self.product
        )
        self.assertEqual(favorite.user.username, 'testuser')
        self.assertEqual(favorite.product.name, 'Smartphone')
        self.assertEqual(str(favorite), 'Избранное пользователь testuser | товар Smartphone')