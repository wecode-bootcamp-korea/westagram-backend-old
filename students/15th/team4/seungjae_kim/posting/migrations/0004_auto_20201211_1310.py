# Generated by Django 3.1.4 on 2020-12-11 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20201211_1310'),
        ('posting', '0003_auto_20201209_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='likes',
            field=models.ManyToManyField(related_name='likers', to='user.Users'),
        ),
        migrations.AlterModelTable(
            name='comments',
            table='comments',
        ),
        migrations.AlterModelTable(
            name='posts',
            table='posts',
        ),
    ]
