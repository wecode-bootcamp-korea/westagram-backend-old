# Generated by Django 3.1.5 on 2021-02-03 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0004_likeposting'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='level',
            field=models.IntegerField(default=1),
        ),
    ]
