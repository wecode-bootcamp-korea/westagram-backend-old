# Generated by Django 3.1.3 on 2020-11-08 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_postimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postimage',
            name='updated_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='postimage',
            name='upload_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
