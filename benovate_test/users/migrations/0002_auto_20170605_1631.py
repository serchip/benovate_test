# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-05 16:31
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='INN',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(999999999999)], verbose_name='ИНН'),
        ),
    ]
