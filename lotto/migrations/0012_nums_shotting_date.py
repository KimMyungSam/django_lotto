# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-19 09:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lotto', '0011_auto_20171113_0016'),
    ]

    operations = [
        migrations.AddField(
            model_name='nums',
            name='shotting_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
