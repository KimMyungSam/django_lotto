# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-19 11:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lotto', '0013_auto_20171119_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nums',
            name='shotDate',
            field=models.DateTimeField(),
        ),
    ]
