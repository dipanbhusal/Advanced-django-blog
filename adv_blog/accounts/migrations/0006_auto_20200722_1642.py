# Generated by Django 3.0.8 on 2020-07-22 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20200722_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(default='accounts/profile_pics/default.jpg', upload_to='accounts/profile_pics/'),
        ),
    ]
