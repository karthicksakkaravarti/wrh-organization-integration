# Generated by Django 4.1.4 on 2023-01-28 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cycling_org', '0045_eventattachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='usac_license_number',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]