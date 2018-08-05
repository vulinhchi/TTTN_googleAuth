# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-05 14:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='Captcha',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='picture/')),
                ('code_captcha', models.CharField(max_length=250, verbose_name='code_captcha')),
            ],
        ),
    ]