# Generated by Django 2.2.16 on 2023-04-05 09:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_post_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='estimation',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
    ]
