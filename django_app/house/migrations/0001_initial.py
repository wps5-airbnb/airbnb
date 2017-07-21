# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-20 14:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=100)),
                ('address', models.TextField(max_length=200)),
                ('introduce', models.TextField(max_length=500)),
                ('space_info', models.TextField(max_length=500)),
                ('guest_access', models.TextField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='HouseImage')),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='house.House')),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extra_people_fee', models.IntegerField()),
                ('cleaning_fee', models.IntegerField()),
                ('weekly_discount', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Space',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accommodates', models.IntegerField()),
                ('bathrooms', models.IntegerField()),
                ('bedrooms', models.IntegerField()),
                ('beds', models.IntegerField()),
                ('room_type', models.CharField(choices=[('집전체', 'house'), ('개인실', 'individual'), ('다인실', 'shared_room')], default='집전체', max_length=3)),
            ],
        ),
    ]
