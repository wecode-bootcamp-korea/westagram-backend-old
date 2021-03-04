# Generated by Django 3.1.5 on 2021-02-07 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_auto_20210202_0953'),
        ('Posting', '0002_usercomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='userposting',
            name='like',
            field=models.ManyToManyField(blank=True, related_name='Userlike', to='User.Userinfo'),
        ),
        migrations.CreateModel(
            name='Userlike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Posting.userposting')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='User.userinfo')),
            ],
            options={
                'db_table': 'userlike',
            },
        ),
    ]
