# Generated by Django 5.0.1 on 2024-02-29 14:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0004_remove_venue_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='VenueImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='venue-images')),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='venue.venue')),
            ],
        ),
    ]