# Generated by Django 4.0.1 on 2022-11-08 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_agegroup_genres_rename_mail_user_mail_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='Age_group_ID',
            new_name='Age_group',
        ),
    ]