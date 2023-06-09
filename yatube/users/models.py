# from django.contrib.auth.models import AbstractUser
# from django.db import models


# class CustomUser(AbstractUser):
#     TYPE = (
#         ('Хозяйство', 'Хозяйство'),
#         ('Пользователь', 'Пользователь')
#     )

#     fio = models.CharField('ФИО, название', max_length=255, default='')
#     type = models.CharField('Тип', max_length=20, choices=TYPE, default='')
#     check = models.BooleanField('Проверка', default=False)
#     location = models.CharField('Расположение', max_length=120, default='')