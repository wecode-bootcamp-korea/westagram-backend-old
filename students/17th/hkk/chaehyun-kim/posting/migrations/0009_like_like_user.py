# Generated by Django 3.1.5 on 2021-02-08 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0008_remove_like_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='like_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='posting.userlike'),
        ),
    ]
