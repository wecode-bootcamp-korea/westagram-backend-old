# Generated by Django 3.1.5 on 2021-02-02 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_user_salt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='salt',
            field=models.CharField(default='', max_length=500),
        ),
    ]
