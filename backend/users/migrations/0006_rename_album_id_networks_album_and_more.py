# Generated by Django 5.0.4 on 2024-07-25 07:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_rename_album_id_photos_album'),
    ]

    operations = [
        migrations.RenameField(
            model_name='networks',
            old_name='album_id',
            new_name='album',
        ),
        migrations.RenameField(
            model_name='networks',
            old_name='user_id',
            new_name='user',
        ),
    ]
