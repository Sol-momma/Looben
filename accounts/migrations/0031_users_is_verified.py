# Generated by Django 4.0.6 on 2022-11-23 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0030_alter_followforuser_table_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
