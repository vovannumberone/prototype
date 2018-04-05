# Generated by Django 2.0 on 2018-04-05 15:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('postmaker', '0005_auto_20180402_1657'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConnectedPublic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.IntegerField(unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SourcePublic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.IntegerField(unique=True)),
                ('index', models.IntegerField(null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='account',
            name='publics',
        ),
        migrations.AddField(
            model_name='account',
            name='balance',
            field=models.IntegerField(null=True),
        ),
    ]
