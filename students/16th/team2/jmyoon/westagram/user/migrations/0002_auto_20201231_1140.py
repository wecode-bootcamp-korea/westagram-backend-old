# Generated by Django 3.1.4 on 2020-12-31 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=40, unique=True)),
                ('phone', models.CharField(max_length=40, unique=True)),
                ('name', models.CharField(max_length=40)),
                ('user_name', models.CharField(max_length=40, unique=True)),
                ('password', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.DeleteModel(
            name='Account',
        ),
    ]