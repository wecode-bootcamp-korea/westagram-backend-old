# Generated by Django 3.1.3 on 2020-11-15 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0003_auto_20201115_2337'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='content',
            new_name='comment',
        ),
    ]