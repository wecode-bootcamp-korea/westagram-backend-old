# Generated by Django 3.1.2 on 2020-10-14 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('tel', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('password', models.IntegerField()),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
