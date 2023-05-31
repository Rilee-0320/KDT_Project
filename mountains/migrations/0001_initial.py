# Generated by Django 3.2.18 on 2023-05-31 10:38

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('crs_name', models.CharField(max_length=30)),
                ('is_waypoint', models.BooleanField(default=False)),
                ('waypoint_name', models.CharField(max_length=50)),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(srid=4326)),
            ],
            options={
                'db_table': 'test_course',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Mountain',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('subname', models.CharField(max_length=200)),
                ('height', models.FloatField()),
                ('region', models.CharField(max_length=100)),
                ('diff', models.CharField(max_length=30)),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(srid=4326)),
            ],
            options={
                'db_table': 'mountains',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
