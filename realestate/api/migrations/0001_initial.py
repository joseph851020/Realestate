# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApiKeys',
            fields=[
                ('description', models.CharField(max_length=100, blank=True, default='', verbose_name='Description')),
                ('key', models.CharField(serialize=False, max_length=40, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'API Keys',
                'verbose_name': 'API Key',
            },
        ),
    ]
