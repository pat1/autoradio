# Generated by Django 3.1.13 on 2024-04-05 18:53

import autoradio.playlists.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0002_auto_20180721_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configure',
            name='sezione',
            field=models.CharField(default='playlist', editable=False, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='giorno',
            name='name',
            field=models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], help_text='weekday name', max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='file',
            field=autoradio.playlists.models.DeletingFileField(help_text='The playlist file to upload, format should be extm3u, m3u, pls', max_length=255, upload_to='playlist', verbose_name='File'),
        ),
    ]
