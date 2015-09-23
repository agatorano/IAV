# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IAV',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('z_score', models.TextField(null=True, blank=True)),
                ('docfile_iav', models.FileField(upload_to=b'IAV/documents/%Y/%m/%d')),
                ('screens', models.IntegerField(default=0)),
                ('flu_proteins', models.TextField(null=True, blank=True)),
                ('word_search', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sess_IAV',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AddField(
            model_name='iav',
            name='sess',
            field=models.ForeignKey(default=None, to='IAV_page.Sess_IAV'),
        ),
    ]
