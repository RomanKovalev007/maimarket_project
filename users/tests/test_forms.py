from django.test import TestCase, Client, override_settings
from users.forms import (
    LoginUserForm,
    RegisterForm,
    ProfileUserDataChangeForm,
    VerificationForm
)
from django.contrib.auth import get_user_model
import tempfile
import shutil

User = get_user_model()


MEDIA_ROOT = tempfile.mkdtemp()

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class FormsTest(TestCase):
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
    def test_login_form(self):
        form_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        form = LoginUserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_register_form(self):
        form_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123'
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_profile_form(self):
        user = User.objects.create_user(username='testuser1', email='test1@example.com')
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'number': '1234567890',
            'telegram': 'johndoe'
        }
        form = ProfileUserDataChangeForm(data=form_data, instance=user)
        self.assertTrue(form.is_valid())

    def test_verification_form(self):
        form_data = {'code': '123456'}
        form = VerificationForm(data=form_data)
        self.assertTrue(form.is_valid())