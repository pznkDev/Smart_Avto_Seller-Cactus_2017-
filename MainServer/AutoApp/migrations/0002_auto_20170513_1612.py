# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-13 16:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AutoApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model',
            name='mark',
            field=models.CharField(max_length=200),
        ),
    ]
