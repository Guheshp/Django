# Generated by Django 5.0.1 on 2024-02-20 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0024_remove_contact_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='email',
            new_name='user_email',
        ),
    ]
