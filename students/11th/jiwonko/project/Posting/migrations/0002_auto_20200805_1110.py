# Generated by Django 3.0.8 on 2020-08-05 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posting', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='img_url',
            field=models.CharField(default='', max_length=1000),
        ),
    ]