# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-06-08 21:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multilingual_survey', '0002_auto_20160405_2039'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyresponse',
            name='ip_address',
            field=models.CharField(blank=True, max_length=32, verbose_name='IP Address'),
        ),
    ]