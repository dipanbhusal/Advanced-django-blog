# Generated by Django 3.0.8 on 2020-07-22 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
