# Generated by Django 3.1.5 on 2021-02-13 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0012_commentoncomment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='parent_comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='posting.comment'),
        ),
        migrations.DeleteModel(
            name='CommentOnComment',
        ),
    ]
