# Generated by Django 3.1.4 on 2021-01-05 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20210105_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
