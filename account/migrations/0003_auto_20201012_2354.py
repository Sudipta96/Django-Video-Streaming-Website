# Generated by Django 2.2.4 on 2020-10-12 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='follower_count',
            field=models.IntegerField(default='0'),
        ),
        migrations.AddField(
            model_name='follow',
            name='following_count',
            field=models.IntegerField(default='0'),
        ),
    ]
