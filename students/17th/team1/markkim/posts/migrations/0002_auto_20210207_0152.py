# Generated by Django 3.1.5 on 2021-02-06 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='post_caption',
            new_name='caption',
        ),
    ]