# Generated by Django 5.0.1 on 2024-03-07 06:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0029_restrictions_servicecategory_remove_amenities_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venue',
            name='amenitie',
        ),
        migrations.RemoveField(
            model_name='venue',
            name='restriction',
        ),
        migrations.CreateModel(
            name='VenueAmenities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amenitie', models.ManyToManyField(to='venue.amenities')),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amenity_name', to='venue.venue')),
            ],
        ),
        migrations.CreateModel(
            name='VenueRestrictions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restrictions', models.ManyToManyField(to='venue.restrictions')),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restrictions_name', to='venue.venue')),
            ],
        ),
    ]
