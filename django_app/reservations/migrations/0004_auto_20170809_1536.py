# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-09 15:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0003_auto_20170809_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservations',
            name='house',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='house.House'),
        ),
        migrations.AlterField(
            model_name='reservations',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
