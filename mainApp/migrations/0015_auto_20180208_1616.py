# Generated by Django 2.0.2 on 2018-02-08 16:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0014_auto_20180208_0849'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificatesmodel',
            name='user',
        ),
        migrations.AddField(
            model_name='userprofilemodel',
            name='certificate',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='datesmodel',
            name='subCourse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dates', to='mainApp.SubCoursesModel'),
        ),
        migrations.DeleteModel(
            name='CertificatesModel',
        ),
    ]