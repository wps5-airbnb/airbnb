# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-20 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0002_auto_20170720_1426'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='house',
            name='price',
        ),
        migrations.RemoveField(
            model_name='house',
            name='space',
        ),
        migrations.AddField(
            model_name='house',
            name='accommodates',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='house',
            name='bathrooms',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='house',
            name='bedrooms',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='house',
            name='beds',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='house',
            name='cleaning_fee',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='house',
            name='extra_people_fee',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='house',
            name='price_per_day',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='house',
            name='room_type',
            field=models.CharField(choices=[('집전체', 'house'), ('개인실', 'individual'), ('다인실', 'shared_room')], default='집전체', max_length=3),
        ),
        migrations.AddField(
            model_name='house',
            name='weekly_discount',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Price',
        ),
        migrations.DeleteModel(
            name='Space',
        ),
    ]
