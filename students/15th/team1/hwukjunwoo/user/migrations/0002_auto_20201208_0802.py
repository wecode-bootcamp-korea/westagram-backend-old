# Generated by Django 3.1.4 on 2020-12-08 08:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='user_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='phone_number',
            new_name='phone',
        ),
    ]
