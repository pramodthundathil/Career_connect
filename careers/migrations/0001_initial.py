# Generated by Django 5.0.1 on 2024-02-12 03:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Joblist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Job_title', models.CharField(max_length=255)),
                ('job_description', models.CharField(max_length=255)),
                ('Salary_start', models.IntegerField()),
                ('Salary_end', models.IntegerField()),
                ('Location', models.CharField(max_length=255)),
                ('mode_of_work', models.CharField(choices=[('Full time', 'Full time'), ('Part Time', 'Part Time'), ('Trainee', 'Trainee')], max_length=255)),
                ('approval_status', models.BooleanField(default=False)),
                ('recruiter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]