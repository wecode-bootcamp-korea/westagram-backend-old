# Generated by Django 3.1.3 on 2020-11-08 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_name', models.CharField(max_length=45)),
                ('img_url', models.CharField(max_length=45)),
                ('img_format', models.IntegerField(default=0)),
                ('img_size', models.CharField(max_length=30)),
                ('upload_date', models.DateTimeField()),
                ('updated_date', models.DateTimeField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.post')),
            ],
            options={
                'db_table': 'postimages',
            },
        ),
    ]