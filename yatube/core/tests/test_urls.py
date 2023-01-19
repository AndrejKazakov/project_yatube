from django.contrib.auth import get_user_model
from django.test import TestCase, Client

User = get_user_model()


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username='test_user')
        cls.guest_client = Client()

    def test_page_uses_corrected_404_template(self):
        """Доступ к шаблону 404"""
        response = self.guest_client.get('/unexisting-page/')
        self.assertTemplateUsed(response, 'core/404.html')
