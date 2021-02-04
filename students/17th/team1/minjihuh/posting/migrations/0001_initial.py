# Generated by Django 3.1.5 on 2021-02-04 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0010_auto_20210204_1043'),
    ]

    operations = [
        migrations.CreateModel(
            name='Posting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.CharField(max_length=2000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(max_length=100, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'db_table': 'postings',
            },
        ),
    ]
