# Generated by Django 3.1.5 on 2021-02-01 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20210201_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='mobile_number',
            field=models.CharField(max_length=14, null=True),
        ),
    ]
