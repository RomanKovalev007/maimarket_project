from io import BytesIO

from PIL import Image
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from goods.forms import AdForm, GoodsFilterForm
from goods.models import Categories, Address, Condition
from users.models import User
import tempfile
import shutil



MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class GoodsFormsTest(TestCase):
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
        self.category = Categories.objects.create(name='Electronics')
        self.address = Address.objects.create(
            name='Moscow',
            address='Red Square',
            link_to_map='https://maps.example.com'
        )
        self.condition = Condition.objects.create(name='New')

        # Создаем валидное тестовое изображение
        self.test_image = self.create_test_image()

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

    def test_ad_form_valid(self):
        form_data = {
            'name': 'Test Product',
            'category': self.category.id,
            'address': self.address.id,
            'condition': self.condition.id,
            'description': 'Test description',
            'price': 1000
        }
        files = {
            'image': self.test_image
        }
        form = AdForm(data=form_data, files=files)

        self.assertTrue(form.is_valid(),
                        f"Form errors: {form.errors}")


    def test_ad_form_invalid(self):
        form_data = {
            'name': '',
            'price': -100
        }
        form = AdForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6)  # name, category, address, condition, image, price

    def test_filter_form_valid(self):
        form_data = {
            'query': 'phone',
            'category': self.category.id,
            'min_price': 500,
            'max_price': 1500
        }
        form = GoodsFilterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_filter_form_empty(self):
        form = GoodsFilterForm(data={})
        self.assertTrue(form.is_valid())