# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-06 14:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ta_logistics_application', '0012_applicationfields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationfields',
            name='allow_multiple',
            field=models.BooleanField(),
        ),
    ]
