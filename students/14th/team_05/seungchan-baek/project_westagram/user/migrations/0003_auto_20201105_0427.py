# Generated by Django 3.1.3 on 2020-11-05 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20201104_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.IntegerField(default=0),
        ),
    ]
