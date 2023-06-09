from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(
        'Заголовок',
        max_length=40,
        help_text='Основная цель мероприятия',
        null=True,
        blank=True
    )
    text = models.TextField(
        'Текст поста',
        help_text='Текст нового поста',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Группа',
        help_text='Группа, к которой будет относиться пост',
        related_name='posts',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
    )
    address = models.CharField(
        'Адрес',
        max_length=200,
        blank=True,
        null=True,
        help_text='Адрес, где будет проводиться данное мероприятие')
    cost = models.IntegerField(
        'Цена',
        max_length=50,
        blank=True,
        null=True,
        help_text='Цена, с указанием денежной валюты'
    )
    end_date = models.DateField(
        'Дата окончания',
        null=True,
        blank=True,
        help_text='Дата окончания мероприятия'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    # estimation = models.IntegerField(
    #     validators=[
    #         MaxValueValidator(100),
    #         MinValueValidator(1)
    #     ],
    #     null=True,
    #     blank=True
    # )
    text = models.TextField(
        'Текст комментария',
        help_text='Текст комментария'
    )
    created = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    def __str__(self):
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )
