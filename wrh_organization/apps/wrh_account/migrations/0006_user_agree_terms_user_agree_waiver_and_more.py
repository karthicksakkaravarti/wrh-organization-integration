# Generated by Django 4.1.4 on 2023-03-04 17:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wrh_account', '0005_auto_20230130_0725'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='agree_terms',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='agree_waiver',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='agreement_waiver_agree_date',
            field=models.DateTimeField(default=datetime.datetime.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='opt_in_email',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='opt_in_email_agree_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='privacy_policy_agree_date',
            field=models.DateTimeField(default=datetime.datetime.now),
            preserve_default=False,
        ),
    ]