# Generated by Django 3.1 on 2020-09-04 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.URLField()),
            ],
        ),
        migrations.AlterField(
            model_name='posting',
            name='published_date',
            field=models.DateTimeField(verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='posting',
            name='images',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posting.images'),
        ),
    ]
