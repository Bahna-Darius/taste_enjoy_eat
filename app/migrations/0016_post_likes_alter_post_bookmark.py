# Generated by Django 4.2.7 on 2023-12-23 12:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0015_post_bookmark'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, default=None, related_name='post_like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='bookmark',
            field=models.ManyToManyField(blank=True, default=None, related_name='bookmarks', to=settings.AUTH_USER_MODEL),
        ),
    ]