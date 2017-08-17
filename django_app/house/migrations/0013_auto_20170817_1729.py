# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-17 17:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0012_holidays'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisabledDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='house',
            name='disabled_days',
            field=models.ManyToManyField(related_name='disabled_day_manager', to='house.DisabledDay'),
        ),
    ]
