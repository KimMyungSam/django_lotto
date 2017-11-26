# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-26 09:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lotto', '0026_auto_20171126_0330'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shootnumbers',
            old_name='predict_total_std',
            new_name='predict_total_25',
        ),
        migrations.AddField(
            model_name='shootnumbers',
            name='predict_total_75',
            field=models.IntegerField(default=0),
        ),
    ]