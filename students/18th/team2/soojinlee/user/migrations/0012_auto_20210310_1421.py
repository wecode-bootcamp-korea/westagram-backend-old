# Generated by Django 3.1.7 on 2021-03-10 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_auto_20210310_0746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
