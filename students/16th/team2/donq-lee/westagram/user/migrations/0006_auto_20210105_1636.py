# Generated by Django 3.1.4 on 2021-01-05 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20210105_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.IntegerField(null=True),
        ),
    ]
