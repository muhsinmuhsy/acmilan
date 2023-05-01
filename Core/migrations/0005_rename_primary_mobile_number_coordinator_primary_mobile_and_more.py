# Generated by Django 4.1.5 on 2023-04-15 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0004_coordinator'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coordinator',
            old_name='primary_mobile_number',
            new_name='primary_mobile',
        ),
        migrations.RenameField(
            model_name='coordinator',
            old_name='secondary_mobile_number',
            new_name='secondary_mobile',
        ),
        migrations.RemoveField(
            model_name='coordinator',
            name='email',
        ),
        migrations.RemoveField(
            model_name='coordinator',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='coordinator',
            name='last_name',
        ),
    ]
