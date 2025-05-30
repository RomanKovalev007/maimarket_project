from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.core import mail
from django.contrib.auth import get_user_model
import tempfile
import shutil

User = get_user_model()


MEDIA_ROOT = tempfile.mkdtemp()

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class RegistrationTest(TestCase):
    @classmethod
    def tearDownClass(cls):
        """Удаляем временную папку с медиафайлами после всех тестов"""
        super().tearDownClass()
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.client = Client()

    def test_register_flow(self):
        # Step 1: Register
        response = self.client.post(reverse('users:register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to verify

        # Check email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Код подтверждения')

        # Get verification code from session
        session = self.client.session
        verification_code = session['temp_user']['code']

        # Step 2: Verify
        response = self.client.post(reverse('users:verify_email'), {
            'code': verification_code
        })
        self.assertEqual(response.status_code, 302)  # Redirect to register_done

        # Check user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())