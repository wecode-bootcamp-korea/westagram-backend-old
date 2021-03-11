# Generated by Django 3.1.7 on 2021-03-11 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_remove_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(default=2, max_length=50, unique=True),
            preserve_default=False,
        ),
    ]
