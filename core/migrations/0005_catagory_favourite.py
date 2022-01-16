# Generated by Django 2.2.4 on 2020-10-14 15:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_catagory_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='catagory',
            name='favourite',
            field=models.ManyToManyField(blank=True, default=None, related_name='favourite', to=settings.AUTH_USER_MODEL),
        ),
    ]