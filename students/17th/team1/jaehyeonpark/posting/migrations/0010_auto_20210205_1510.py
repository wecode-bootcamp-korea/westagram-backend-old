# Generated by Django 3.1.5 on 2021-02-05 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0009_auto_20210205_1313'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together=set(),
        ),
    ]
