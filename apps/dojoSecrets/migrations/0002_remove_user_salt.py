# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-25 19:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dojoSecrets', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='salt',
        ),
    ]
