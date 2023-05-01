# Generated by Django 4.1.5 on 2023-04-13 22:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_number', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('contact_info', models.CharField(max_length=200)),
                ('num_students', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_number', models.CharField(max_length=10, unique=True)),
                ('full_name', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('zipcode', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('date_of_birth', models.DateField()),
                ('preferred_location', models.CharField(max_length=100)),
                ('street_address', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=20)),
                ('guardian_name', models.CharField(max_length=100)),
                ('guardian_phone_number', models.CharField(max_length=20)),
                ('id_proof', models.ImageField(upload_to='id_proof/')),
                ('age_group', models.CharField(max_length=100)),
                ('mode_of_travel', models.CharField(max_length=100)),
                ('football_playing_position', models.CharField(max_length=100)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.branch')),
            ],
        ),
    ]
