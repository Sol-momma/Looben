# Generated by Django 4.0.6 on 2022-11-18 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0012_remove_blog_total_number_of_view_blog_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='total_number_of_view',
            field=models.IntegerField(default=0),
        ),
    ]