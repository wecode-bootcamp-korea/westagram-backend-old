# Generated by Django 3.1.3 on 2020-11-12 06:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20201111_1610'),
        ('follow', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='follow_user', to='user.user'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='be_followed',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='followed_user', to='user.user'),
        ),
    ]
