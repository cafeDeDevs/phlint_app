# Generated by Django 5.0.4 on 2024-07-30 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_user_user_email_user_email_user_groups_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_password',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]