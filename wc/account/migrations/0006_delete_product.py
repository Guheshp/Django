# Generated by Django 5.0.1 on 2024-02-04 07:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_remove_vendor_user_vendor_vender_address_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Product',
        ),
    ]
