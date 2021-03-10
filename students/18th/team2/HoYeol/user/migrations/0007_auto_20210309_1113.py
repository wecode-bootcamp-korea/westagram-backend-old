# Generated by Django 3.1.7 on 2021-03-09 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20210308_1001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='pswd',
        ),
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default=None, max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
