# Generated by Django 4.0.6 on 2022-09-29 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_questions_is_solved'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='is_anonymous',
            field=models.BooleanField(default=False),
        ),
    ]
