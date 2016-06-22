# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-21 18:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion

from filer.settings import FILER_IMAGE_MODEL


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0004_auto_20160328_1434'),
    ]

    if not FILER_IMAGE_MODEL:
        operations = [
            migrations.AlterField(
                model_name='image',
                name='file_ptr',
                field=models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    primary_key=True,
                    related_name='+',
                    serialize=False,
                    to='filer.File'
                ),
            ),
        ]
