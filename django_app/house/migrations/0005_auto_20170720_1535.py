# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-20 15:35
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0004_auto_20170720_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='weekly_discount',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
