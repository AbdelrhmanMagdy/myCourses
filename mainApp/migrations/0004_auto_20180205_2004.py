# Generated by Django 2.0.2 on 2018-02-05 20:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0003_auto_20180205_1916'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='centremodel',
            name='centreImages',
        ),
        migrations.AddField(
            model_name='centreimagesmodel',
            name='centre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='mainApp.CentreModel'),
        ),
    ]
