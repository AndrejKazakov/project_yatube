# Generated by Django 2.2.16 on 2023-04-05 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_auto_20230312_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='address',
            field=models.CharField(blank=True, help_text='Адрес, где будет проводиться данное мероприятие', max_length=200, null=True, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='post',
            name='cost',
            field=models.CharField(blank=True, help_text='Цена, с указанием денежной валюты', max_length=50, null=True, verbose_name='Цена'),
        ),
    ]