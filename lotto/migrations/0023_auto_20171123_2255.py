# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-23 13:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lotto', '0022_auto_20171123_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='decidednumbers',
            name='band',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='decidednumbers',
            name='blue',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='decidednumbers',
            name='bonus',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='decidednumbers',
            name='count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='decidednumbers',
            name='end_digit',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='decidednumbers',
            name='even',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='decidednumbers',
            name='five',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='decidednumbers',
            name='four',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='decidednumbers',
            name='four_continue',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='decidednumbers',
            name='gray',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='decidednumbers',
            name='green',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='decidednumbers',
            name='odd',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='decidednumbers',
            name='one',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='decidednumbers',
            name='one_continue',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='decidednumbers',
            name='person',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='decidednumbers',
            name='red',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='decidednumbers',
            name='six',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='decidednumbers',
            name='three',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='decidednumbers',
            name='three_continue',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='decidednumbers',
            name='total',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='decidednumbers',
            name='two',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='decidednumbers',
            name='two_continue',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='decidednumbers',
            name='yellow',
            field=models.IntegerField(default=0),
        ),
    ]