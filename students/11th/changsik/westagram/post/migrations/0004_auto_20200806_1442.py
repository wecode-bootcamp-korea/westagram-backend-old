# Generated by Django 3.0.8 on 2020-08-06 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_auto_20200805_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(max_length=300),
        ),
    ]
