from django.contrib.auth import get_user_model
from posts.models import Group, Post
from django.test import TestCase, Client
from http import HTTPStatus
from django.urls import reverse

User = get_user_model()


class StaticURLTests(TestCase):

    def setUp(self):
        self.guest_client = Client()

    def test_homepage(self):
        response = self.guest_client.get(reverse('posts:index'))
        self.assertEqual(response.status_code, HTTPStatus.OK)


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username='test_user')
        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовый текст'
        )
        cls.post = Post.objects.create(
            text='Тестовая запись',
            pub_date='Тестовая дата',
            author=cls.user,
            group=cls.group
        )

    def test_url_exists_at_desired_location(self):
        """Доступ к общим страницам"""
        url_names = {
            reverse('posts:index'): HTTPStatus.OK,
            reverse('posts:group_list',
                    kwargs={'slug': 'test_slug'}): HTTPStatus.OK,
            reverse('posts:profile',
                    kwargs={'username': self.post.author}): HTTPStatus.OK,
            reverse('posts:post_detail',
                    kwargs={'post_id': self.post.id}): HTTPStatus.OK,
        }
        for address, http_status in url_names.items():
            with self.subTest(http_status=http_status):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, http_status)

    def test_url_exists_at_page_with_auth(self):
        """Доступ к страницам с авторизацией"""
        url_names = {
            reverse('posts:post_create'): HTTPStatus.OK,
            reverse('posts:post_edit',
                    kwargs={'post_id': self.post.id}): HTTPStatus.OK,
        }
        for address, http_status in url_names.items():
            with self.subTest(http_status=http_status):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, http_status)

    def test_pages_uses_corrected_template(self):
        """Доступ к шаблонам"""
        url_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list',
                    kwargs={'slug': 'test_slug'}): 'posts/group_list.html',
            reverse(
                'posts:profile', kwargs={'username': self.post.author}
            ): 'posts/profile.html',
            reverse(
                'posts:post_detail', kwargs={'post_id': self.post.id}
            ): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.id}): 'posts/create_post.html',
        }
        for address, template in url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_unexisting_page(self):
        """Доступ к несуществующей странице"""
        response = self.authorized_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_post_create_url_redirect_anonymous_on_admin_login(self):
        """Страница по адресу /create/ переправит анонимного
        пользователя на страницу логина.
        """
        response = self.guest_client.get(
            reverse('posts:post_create'),
            follow=True
        )
        self.assertRedirects(response, '/auth/login/?next=/create/')

    def test_post_edit_url_redirect_anonymous_on_admin_login(self):
        """Страница по адресу /edit/ переправит анонимного
        пользователя на страницу логина.
        """
        response = self.guest_client.get(
            reverse('posts:post_edit',
                    kwargs={'post_id': self.post.id}), follow=True)
        self.assertRedirects(
            response, (f'/auth/login/?next=/posts/{self.post.id}/edit/')
        )

    def test_post_edit_url_with_author(self):
        """Доступ на редактирование поста"""
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
