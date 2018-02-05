# Generated by Django 2.0.2 on 2018-02-04 00:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfileModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=11)),
                ('educationLevel', models.CharField(choices=[('university', 'university'), ('highSchool', 'highSchool'), ('school', 'school')], max_length=15)),
                ('university', models.CharField(blank=True, max_length=15)),
                ('faculty', models.CharField(blank=True, max_length=15)),
                ('major', models.CharField(blank=True, max_length=15)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
