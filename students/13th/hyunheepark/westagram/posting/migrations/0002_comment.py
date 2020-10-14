# Generated by Django 3.1.1 on 2020-10-14 21:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20201013_1649'),
        ('posting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment_content', models.TextField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posting.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'db_table': 'comments',
            },
        ),
    ]
