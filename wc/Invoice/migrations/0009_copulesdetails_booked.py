# Generated by Django 5.0.1 on 2024-03-18 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Invoice', '0008_copulesdetails_advance_paid_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='copulesdetails',
            name='booked',
            field=models.BooleanField(default=False),
        ),
    ]
