# Generated by Django 3.1.5 on 2021-02-09 02:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0007_auto_20210208_0508'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='root',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='posting.comment'),
        ),
    ]