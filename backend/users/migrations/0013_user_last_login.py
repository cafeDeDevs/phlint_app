# Generated by Django 5.0.4 on 2024-08-13 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0012_rename_s3_url_albums_album_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="last_login",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
