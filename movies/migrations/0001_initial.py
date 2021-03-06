# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-15 17:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200, verbose_name='Movie name')),
                ('rows', models.PositiveSmallIntegerField(default=100, verbose_name='Number of rows')),
                ('columns', models.PositiveSmallIntegerField(default=100, verbose_name='Number of columns')),
            ],
        ),
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('row_num', models.PositiveSmallIntegerField()),
                ('col_num', models.PositiveSmallIntegerField()),
                ('status', models.IntegerField(choices=[(1, 'AVAILABLE'), (2, 'BLOCKED'), (3, 'RESERVED')], default=1)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Movie')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='tickets',
            unique_together=set([('movie', 'row_num', 'col_num')]),
        ),
    ]
