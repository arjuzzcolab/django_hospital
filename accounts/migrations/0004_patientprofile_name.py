# Generated by Django 4.2.16 on 2024-10-02 13:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_patientprofile_patient'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientprofile',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
    ]
