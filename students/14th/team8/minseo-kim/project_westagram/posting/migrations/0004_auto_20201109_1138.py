# Generated by Django 3.1.3 on 2020-11-09 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0003_auto_20201108_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content',
            field=models.TextField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='image_url',
            field=models.URLField(null=True),
        ),
    ]