# Generated by Django 3.1.7 on 2021-03-11 04:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_auto_20210311_0403'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
    ]
