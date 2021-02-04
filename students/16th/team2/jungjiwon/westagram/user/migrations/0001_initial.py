# Generated by Django 3.1.4 on 2021-01-04 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=30)),
                ('tel_num', models.CharField(max_length=20)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]