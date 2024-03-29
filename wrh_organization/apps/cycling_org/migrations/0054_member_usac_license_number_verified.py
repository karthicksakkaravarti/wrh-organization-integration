# Generated by Django 4.1.7 on 2023-02-23 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cycling_org', '0053_event_publish_type_event_shared_org_perms'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='usac_license_number_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='member',
            name='usac_license_number',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]
