# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-10 03:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Authenticator',
            fields=[
                ('user_id', models.IntegerField()),
                ('authenticator', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('date_created', models.DateField()),
            ],
        ),
        migrations.AlterField(
            model_name='listing',
            name='buyer',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to='myapp.User'),
        ),
        migrations.AlterField(
            model_name='user',
            name='passwordHash',
            field=models.CharField(max_length=256),
        ),
    ]
