# Generated by Django 4.0.6 on 2022-10-10 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_users_individual_theme_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='individual_theme_color',
            field=models.CharField(default='white', max_length=10),
        ),
    ]