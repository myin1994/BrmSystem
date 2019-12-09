# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-12-05 05:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=18, unique=True)),
                ('password', models.CharField(max_length=32)),
                ('phone_number', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=50)),
            ],
        ),
    ]