# Generated by Django 4.0.6 on 2022-09-17 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_add_number_of_viewer'),
    ]

    operations = [
        migrations.AddField(
            model_name='schools',
            name='star_rating',
            field=models.IntegerField(default=0),
        ),
    ]