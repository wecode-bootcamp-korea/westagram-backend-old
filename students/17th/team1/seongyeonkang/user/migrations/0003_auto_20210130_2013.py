# Generated by Django 3.1.5 on 2021-01-30 20:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210129_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 1, 30, 20, 13, 19, 612680)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2021, 1, 30, 20, 13, 33, 929265)),
            preserve_default=False,
        ),
    ]
