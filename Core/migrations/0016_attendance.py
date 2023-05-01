# Generated by Django 4.2 on 2023-04-29 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0015_delete_attends'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('Attandance', models.CharField(default='Absent', max_length=15)),
                ('Student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Core.student')),
                ('time_section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.timesection')),
            ],
        ),
    ]