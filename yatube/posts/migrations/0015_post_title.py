# Generated by Django 2.2.16 on 2023-04-05 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_auto_20230405_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(blank=True, help_text='Основная цель мероприятия', max_length=40, null=True, verbose_name='Заголовок'),
        ),
    ]
