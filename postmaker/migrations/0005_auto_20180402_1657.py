# Generated by Django 2.0 on 2018-04-02 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('postmaker', '0004_auto_20180402_1653'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='username',
            new_name='user',
        ),
    ]
