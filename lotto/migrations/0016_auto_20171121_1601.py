# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-21 07:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lotto', '0015_auto_20171120_0006'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='nums',
            new_name='DecidedNumbers',
        ),
    ]
