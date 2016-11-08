# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-08 22:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ta_logistics_application', '0012_delete_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('ubit_name', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('person_number', models.CharField(max_length=30)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('semester', models.CharField(max_length=30)),
                ('class_id', models.CharField(max_length=30)),
                ('class_name', models.CharField(max_length=30)),
                ('application_status', models.CharField(max_length=30)),
            ],
        ),
    ]
