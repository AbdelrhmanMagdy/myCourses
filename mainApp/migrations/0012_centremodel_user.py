# Generated by Django 2.0.2 on 2018-02-08 07:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainApp', '0011_remove_userprofilemodel_educationlevel'),
    ]

    operations = [
        migrations.AddField(
            model_name='centremodel',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]