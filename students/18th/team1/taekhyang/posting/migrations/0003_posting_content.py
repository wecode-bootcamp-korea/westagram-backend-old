# Generated by Django 3.1.7 on 2021-03-04 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0002_auto_20210304_1123'),
    ]

    operations = [
        migrations.AddField(
            model_name='posting',
            name='content',
            field=models.CharField(blank=True, max_length=2000),
        ),
    ]
