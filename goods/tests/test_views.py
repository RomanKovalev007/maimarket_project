from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from goods.models import Goods, Categories, Address, Condition
from users.models import User
import tempfile
import shutil


MEDIA_ROOT = tempfile.mkdtemp()

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class GoodsViewsTest(TestCase):
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
        self.category = Categories.objects.create(name='Electronics')
        self.address = Address.objects.create(
            name='Moscow',
            address='Red Square',
            link_to_map='https://maps.example.com'
        )
        self.condition = Condition.objects.create(name='New')

        test_image = SimpleUploadedFile(
            name='test.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00',
            content_type='image/jpeg'
        )
        self.goods = Goods.objects.create(
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

    def test_goods_list_view(self):
        response = self.client.get(reverse('goods:goods_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Smartphone')
        self.assertTemplateUsed(response, 'goods/goods_list.html')

    def test_show_ad_view(self):
        response = self.client.get(reverse('goods:ad', kwargs={'ad_slug': 'smartphone'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test description')
        self.assertTemplateUsed(response, 'goods/product-card.html')

    def test_add_ad_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('goods:add_ad'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'goods/add_ad.html')

    def test_add_ad_view_unauthenticated(self):
        response = self.client.get(reverse('goods:add_ad'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_edit_ad_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('goods:edit', kwargs={'ad_slug': 'smartphone'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'goods/add_ad.html')

    def test_publish_ad_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('goods:publish', kwargs={'ad_slug': 'smartphone'}),
                                   HTTP_REFERER=reverse('goods:ad', kwargs={'ad_slug': 'smartphone'}))
        self.assertEqual(response.status_code, 302)  # Redirect back

        goods = Goods.objects.get(slug='smartphone')
        self.assertFalse(goods.is_published)