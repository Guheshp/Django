# Generated by Django 5.0.1 on 2024-02-20 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0022_content'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='content',
            new_name='Contact',
        ),
    ]