# Generated by Django 4.0.6 on 2022-11-03 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_alter_users_individual_theme_color'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schools',
            old_name='national',
            new_name='is_national',
        ),
    ]