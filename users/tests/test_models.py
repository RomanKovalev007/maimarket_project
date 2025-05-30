from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import User
import os
from django.conf import settings
import tempfile
import shutil



MEDIA_ROOT = tempfile.mkdtemp()

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class UserModelTest(TestCase):
    @classmethod
    def tearDownClass(cls):
        """Удаляем временную папку с медиафайлами после всех тестов"""
        super().tearDownClass()
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('TestPass123'))

    def test_photo_upload(self):
        test_image = SimpleUploadedFile(
            name='test.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00',
            content_type='image/jpeg'
        )
        self.user.photo = test_image
        self.user.save()

        self.assertTrue(os.path.exists(os.path.join(settings.MEDIA_ROOT, self.user.photo.path)))
        os.remove(self.user.photo.path)  # Clean up

    def test_get_absolute_url(self):
        expected_url = f'/users/profile/{self.user.id}/'
        self.assertEqual(self.user.get_absolute_url(), expected_url)

    def test_telegram_field(self):
        self.user.telegram = 'testtelegram'
        self.user.save()
        self.assertEqual(self.user.telegram, 'testtelegram')