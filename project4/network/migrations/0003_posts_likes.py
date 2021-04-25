# Generated by Django 3.1.6 on 2021-04-25 05:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_remove_posts_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='likes',
            field=models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]