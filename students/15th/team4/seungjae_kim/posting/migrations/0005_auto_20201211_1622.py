# Generated by Django 3.1.4 on 2020-12-11 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0004_auto_20201211_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='posts',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
