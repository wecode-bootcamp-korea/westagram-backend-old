# Generated by Django 3.1.7 on 2021-03-08 15:28

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
                ('email', models.EmailField(max_length=50, unique=True)),
                ('phone', models.CharField(max_length=11, null=True, unique=True)),
                ('full_name', models.CharField(max_length=40, null=True)),
                ('user_name', models.CharField(max_length=20, null=True, unique=True)),
                ('password', models.CharField(max_length=70)),
                ('date_of_birth', models.DateField(null=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
