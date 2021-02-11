# Generated by Django 3.0.8 on 2020-08-03 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_auto_20200803_0705'),
        ('Post', '0010_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.User')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Post.Post')),
            ],
        ),
    ]
