import shutil
import tempfile
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.core.cache import cache
from posts.models import Group, Post, Comment, Follow
from django.test import TestCase, Client, override_settings
from django import forms
from django.urls import reverse

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TestView(TestCase):
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

        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )

        cls.post = Post.objects.create(
            text='Тестовая запись 1',
            pub_date='Тестовая дата',
            author=cls.user,
            group=cls.group,
            image=uploaded
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_pages_uses_correct_template(self):
        """URL-адреса используют соответствующие шаблоны"""
        template_pages_name = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group_list',
                kwargs={'slug': 'test_slug'}
            ): 'posts/group_list.html',
            reverse(
                'posts:profile',
                kwargs={'username': self.post.author}
            ): 'posts/profile.html',
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.id}
            ): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.id}
            ): 'posts/create_post.html',
        }
        for reverse_name, template in template_pages_name.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.guest_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author
        post_group_0 = first_object.group
        post_image_0 = first_object.image
        self.assertEqual(post_text_0, self.post.text)
        self.assertEqual(post_author_0, self.post.author)
        self.assertEqual(post_group_0, self.post.group)
        self.assertEqual(post_image_0, self.post.image)

    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.guest_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug})
        )
        first_object = response.context['group']
        group_title_0 = first_object.title
        group_slug_0 = first_object.slug
        post_image_0 = Post.objects.first().image
        self.assertEqual(group_title_0, self.group.title)
        self.assertEqual(group_slug_0, self.group.slug)
        self.assertEqual(post_image_0, self.post.image)

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.guest_client.get(
            reverse('posts:profile', kwargs={'username': self.post.author})
        )
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        post_image_0 = first_object.image
        self.assertEqual(response.context['author'], self.post.author)
        self.assertEqual(post_text_0, self.post.text)
        self.assertEqual(post_image_0, self.post.image)

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.guest_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id})
        )
        post_object = response.context['post']
        post_text_0 = post_object.text
        post_author_0 = post_object.author
        post_group_0 = post_object.group
        post_image_0 = post_object.image
        self.assertEqual(post_text_0, self.post.text)
        self.assertEqual(post_author_0, self.post.author)
        self.assertEqual(post_group_0, self.post.group)
        self.assertEqual(response.context['post'], self.post)
        self.assertEqual(post_image_0, self.post.image)

    def test_create_post_page_show_correct_context(self):
        """Шаблон create_post сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_edit_post_page_show_correct_context(self):
        """Шаблон edit_post сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }
        self.assertEqual(response.context['post'], self.post)
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_create_appears_on_pages_with_group(self):
        """Пост попал при создании в нужную группу и
        отображается на страницах index, post_group, profile
        """
        pages = {
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
            reverse('posts:profile', kwargs={'username': self.post.author})
        }
        for page in pages:
            with self.subTest(page=page):
                response = self.authorized_client.get(page)
                first_object = response.context['page_obj'][0]
                post_text_0 = first_object.text
                post_group_0 = first_object.group
                self.assertEqual(post_text_0, self.post.text)
                self.assertEqual(post_group_0, self.post.group)


class PaginatorViewsTest(TestCase):
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
        cls.post = []
        for i in range(13):
            cls.post.append(Post(
                text=f'Тестовая запись {i}',
                author=cls.user,
                group=cls.group
            )
            )
        Post.objects.bulk_create(cls.post)

    def test_first_second_page_contains_ten_records(self):
        """Проверка количества постов на первой и второй странице"""
        response_page_1 = self.guest_client.get(reverse('posts:index'))
        self.assertEqual(len(response_page_1.context['page_obj']), 10)

        response_page_2 = self.client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response_page_2.context['page_obj']), 3)


class CommentsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username='test_user')
        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.post = Post.objects.create(
            text='Тестовая запись 1',
            pub_date='Тестовая дата',
            author=cls.user
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user,
            text='Тестовый текст',
            created='Тестовая дата'
        )

    def test_create_comment(self):
        """Комментарий появляется на странице
        поста после успешной отправки
        """
        pages = {
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}),
        }
        for page in pages:
            with self.subTest(page=page):
                first_object = Comment.objects.get()
                comment_post = first_object.post
                comment_author = first_object.author
                comment_text = first_object.text
                comment_created = first_object.created
                self.assertEqual(comment_post, self.comment.post)
                self.assertEqual(comment_author, self.comment.author)
                self.assertEqual(comment_text, self.comment.text)
                self.assertEqual(comment_created, self.comment.created)


class CacheTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user')
        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.post = Post.objects.create(
            text='Тестовая запись 1',
            pub_date='Тестовая дата',
            author=cls.user
        )

    def test_cache_index(self):
        """Страница index кэшируется"""
        first_object = self.authorized_client.get(reverse('posts:index'))
        post_1 = Post.objects.get(pk=1)
        post_1.text = 'new_text'
        post_1.save()
        second_object = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(first_object.content, second_object.content)
        cache.clear()
        third_object = self.authorized_client.get(reverse('posts:index'))
        self.assertNotEqual(first_object.content, third_object.content)


class FollowTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client_auth_follower = Client()
        cls.client_auth_following = Client()
        cls.follower = User.objects.create_user(username='follower')
        cls.following = User.objects.create_user(username='following')
        cls.client_auth_follower.force_login(cls.follower)
        cls.client_auth_following.force_login(cls.following)

        cls.post = Post.objects.create(
            text='Тестовая запись 1',
            pub_date='Тестовая дата',
            author=cls.following
        )

    def test_follow_auth(self):
        """Авторизованный пользователь может
        подписаться на автора
        """
        self.client_auth_follower.get(
            reverse(
                'posts:profile_follow',
                kwargs={'username': self.following.username}
            )
        )
        self.assertEqual(Follow.objects.all().count(), 1)

    def test_unfollow_auth(self):
        """Авторизованный пользователь может
        отписаться от автора
        """
        self.client_auth_follower.get(
            reverse(
                'posts:profile_follow',
                kwargs={'username': self.following.username}
            )
        )
        self.client_auth_follower.get(
            reverse(
                'posts:profile_unfollow',
                kwargs={'username': self.following.username}
            )
        )
        self.assertEqual(Follow.objects.all().count(), 0)

    def test_following_post(self):
        """Запись появляется у
        подписанного пользователя
        """
        Follow.objects.create(
            user=self.follower,
            author=self.following
        )
        response = self.client_auth_follower.get(reverse('posts:follow_index'))
        post_text = response.context['page_obj'][0].text
        self.assertEqual(post_text, self.post.text)

    def test_following_post(self):
        """Запись не появляется у
        неподписанного пользователя
        """
        response = self.client_auth_follower.get(
            reverse('posts:follow_index')
        )
        self.assertNotContains(response, self.post.text)
