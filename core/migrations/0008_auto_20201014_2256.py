# Generated by Django 2.2.4 on 2020-10-14 16:56

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_merge_20201014_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catagory',
            name='avatar',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default='default_category_avatar.jpg', null=True, upload_to='catagory_avatar/%Y/%m/%d/'),
        ),
    ]
