# Generated by Django 3.1.3 on 2020-11-08 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_auto_20201109_0228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postimage',
            name='img_format',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='postimage',
            name='img_name',
            field=models.CharField(max_length=100),
        ),
    ]
