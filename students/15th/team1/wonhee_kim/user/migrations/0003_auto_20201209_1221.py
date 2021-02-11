# Generated by Django 3.1.4 on 2020-12-09 03:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20201208_0905'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='from_user', to='user.user')),
                ('to_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='to_user', to='user.user')),
            ],
            options={
                'db_table': 'follows',
                'unique_together': {('from_user', 'to_user')},
            },
        ),
        migrations.AddField(
            model_name='user',
            name='follow',
            field=models.ManyToManyField(through='user.Follow', to='user.User'),
        ),
    ]
