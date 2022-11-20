# Generated by Django 4.0.6 on 2022-11-18 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0011_alter_blog_meta_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='total_number_of_view',
        ),
        migrations.AddField(
            model_name='blog',
            name='tag',
            field=models.CharField(max_length=25, null=True, verbose_name='タグ'),
        ),
    ]
