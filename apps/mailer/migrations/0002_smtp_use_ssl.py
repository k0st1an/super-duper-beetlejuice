# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-14 14:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='smtp',
            name='use_ssl',
            field=models.BooleanField(default=True),
        ),
    ]
