# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-20 19:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ta_logistics_application', '0019_auto_20161115_2140'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayrollInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_ssn', models.BooleanField(choices=[(1, 'Yes'), (0, 'No')], default=0)),
                ('been_ub_employee', models.BooleanField(choices=[(1, 'Yes'), (0, 'No')], default=0)),
                ('been_student_assistant', models.BooleanField(choices=[(1, 'Yes'), (0, 'No')], default=0)),
                ('other_on_campus_job', models.BooleanField(choices=[(1, 'Yes'), (0, 'No')], default=0)),
                ('fall_and_spring', models.BooleanField(choices=[(1, 'Yes'), (0, 'No')], default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='classapplicants',
            name='application_status_id',
        ),
        migrations.AddField(
            model_name='classapplicants',
            name='given_offer',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='classapplicants',
            name='hiring_status_id',
            field=models.IntegerField(choices=[(0, 'Pending Review'), (1, 'Rejected'), (2, 'Interviewing'), (3, 'Given Offer'), (4, 'Wait Listed'), (5, 'Accepted Offer'), (6, 'Declined Offer')], default=0),
        ),
    ]
