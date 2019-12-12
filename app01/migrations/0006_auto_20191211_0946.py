# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-12-11 01:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_consultrecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultrecord',
            name='note',
            field=models.TextField(default='公转私', verbose_name='跟进内容...'),
        ),
        migrations.AlterField(
            model_name='consultrecord',
            name='status',
            field=models.CharField(choices=[('A', '近期无报名计划'), ('B', '1个月内报名'), ('C', '2周内报名'), ('D', '1周内报名'), ('E', '定金'), ('F', '到班'), ('G', '全款'), ('H', '无效'), ('I', '未跟进')], default='I', help_text='选择客户此时的状态', max_length=8, verbose_name='跟进状态'),
        ),
    ]
