# Generated by Django 3.1.2 on 2021-03-31 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20210330_2258'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_picture_url',
            field=models.TextField(default='https://www.flaticon.com/svg/static/icons/svg/847/847969.svg', max_length=300),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.SmallIntegerField(default=4),
        ),
    ]
