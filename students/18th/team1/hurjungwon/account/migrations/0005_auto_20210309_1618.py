# Generated by Django 3.1.7 on 2021-03-09 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20210308_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='follow',
            field=models.ManyToManyField(through='account.Follow', to='account.User'),
        ),
    ]
