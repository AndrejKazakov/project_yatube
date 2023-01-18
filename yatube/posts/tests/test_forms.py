import shutil
import tempfile
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from posts.models import Group, Post, Comment
from django.test import TestCase, Client, override_settings
from http import HTTPStatus
from django.urls import reverse

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TestFroms(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовый текст'
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='test_user')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_post_create(self):
        """Создание поста"""
        form_data = {
            'text': 'test_text',
            'group': self.group.id
        }
        post_count = Post.objects.count()
        response = self.authorized_client.post(
            reverse('posts:post_create'), data=form_data, follow=True)
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': self.user}))
        self.assertEqual(Post.objects.count(), post_count + 1)

        post_object = Post.objects.get(id=self.group.id)
        post_author = User.objects.get(username=self.user)
        post_group = Group.objects.get(title=self.group.title)
        self.assertEqual(post_object.text, form_data['text'])
        self.assertEqual(post_author, self.user)
        self.assertEqual(post_group.title, self.group.title)

    def test_post_edit(self):
        """Изменение поста"""
        form_data = {
            'text': 'test_text',
            'group': self.group.id
        }
        self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )

        post_object = Post.objects.get(id=self.group.id)
        self.client.get(reverse(
            'posts:post_edit',
            kwargs={'post_id': post_object.id}
        ))
        form_data = {
            'text': 'test_edit_text',
            'group': self.group.id
        }
        response_edit = self.authorized_client.post(
            reverse('posts:post_edit',
                    kwargs={
                        'post_id': post_object.id
                    }),
            data=form_data,
            follow=True,
        )
        post_object = Post.objects.get(id=self.group.id)
        self.assertEqual(response_edit.status_code, HTTPStatus.OK)
        self.assertEqual(post_object.text, form_data['text'])

    def test_post_with_img(self):
        """При отправке поста с изображением
        создается запись в БД
        """
        post_count = Post.objects.count()

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
        form_data = {
            'text': 'test_text',
            'group': self.group.id,
            'image': uploaded,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )

        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': self.user}))
        self.assertEqual(Post.objects.count(), post_count + 1)

        post_object = Post.objects.get(id=self.group.id)
        self.assertTrue(
            Post.objects.filter(
                text=post_object.text,
                image=post_object.image,
                group=post_object.group,
                author=post_object.author
            ).exists()
        )

    def test_add_comment(self):
        """Создание комментария"""
        form_data = {
            'text': 'test_text',
            'group': self.group.id
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'), data=form_data, follow=True)
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': self.user}))

        post_object = Post.objects.get(id=self.group.id)
        post_author = User.objects.get(username=self.user)
        post_group = Group.objects.get(title=self.group.title)
        self.assertEqual(post_object.text, form_data['text'])
        self.assertEqual(post_author, self.user)
        self.assertEqual(post_group.title, self.group.title)

        post_count = Comment.objects.count()
        form_data = {
            'text': 'test_text',
            'created': 'test_date',
            'post': post_object.id
        }

        response = self.authorized_client.post(
            reverse(
                'posts:add_comment',
                kwargs={'post_id': post_object.id}
            ),
            data=form_data, follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': post_object.id}))

        first_object = Comment.objects.get()
        comment_post = first_object.post
        comment_author = first_object.author
        comment_text = first_object.text
        comment_created = first_object.created
        self.assertEqual(comment_post, first_object.post)
        self.assertEqual(comment_text, first_object.text)
        self.assertEqual(comment_created, first_object.created)
        self.assertEqual(comment_author, first_object.author)
        self.assertEqual(Comment.objects.count(), post_count + 1)
