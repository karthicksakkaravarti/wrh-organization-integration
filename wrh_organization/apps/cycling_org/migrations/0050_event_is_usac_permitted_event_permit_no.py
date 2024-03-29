# Generated by Django 4.1.4 on 2023-02-05 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cycling_org', '0049_alter_organization_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_usac_permitted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='permit_no',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
