# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-12-16 03:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0003_auto_20191216_1024'),
    ]

    operations = [
        migrations.AddField(
            model_name='topmenu',
            name='weight',
            field=models.IntegerField(default=10),
        ),
    ]