# Generated by Django 3.1.1 on 2020-10-16 02:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0006_auto_20201016_0050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posting',
            name='like',
        ),
    ]