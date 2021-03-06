# Generated by Django 3.1.7 on 2021-03-05 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20210304_1120'),
        ('posting', '0003_posting_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posting',
            name='content',
            field=models.CharField(max_length=2000),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('content', models.CharField(max_length=2000)),
                ('posting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posting.posting')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.user')),
            ],
        ),
    ]