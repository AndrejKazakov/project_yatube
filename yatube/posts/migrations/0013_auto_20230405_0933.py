# Generated by Django 2.2.16 on 2023-04-05 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_post_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата окончания'),
        ),
    ]
