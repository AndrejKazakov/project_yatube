# Generated by Django 4.2 on 2023-04-05 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0017_remove_comment_estimation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='cost',
            field=models.IntegerField(blank=True, help_text='Цена, с указанием денежной валюты', max_length=50, null=True, verbose_name='Цена'),
        ),
    ]
