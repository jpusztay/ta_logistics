# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-11 22:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ta_logistics_application', '0023_auto_20161211_0442'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classapplicants',
            name='pending_offer',
        ),
    ]