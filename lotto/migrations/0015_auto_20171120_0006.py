# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-19 15:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lotto', '0014_auto_20171119_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nums',
            name='shotDate',
            field=models.DateField(),
        ),
    ]
