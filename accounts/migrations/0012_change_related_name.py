# Generated by Django 4.0.6 on 2022-09-01 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_add_saved_university'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='saved_university',
            field=models.ManyToManyField(blank=True, related_name='saved_university_users', to='accounts.schools'),
        ),
    ]