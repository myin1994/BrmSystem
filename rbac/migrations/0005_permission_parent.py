# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-12-16 06:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0004_topmenu_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.Permission'),
        ),
    ]