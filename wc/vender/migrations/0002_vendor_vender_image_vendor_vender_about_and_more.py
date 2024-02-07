# Generated by Django 5.0.1 on 2024-02-04 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vender', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='Vender_image',
            field=models.ImageField(default='defaultvenderimg.png', null=True, upload_to='uploads'),
        ),
        migrations.AddField(
            model_name='vendor',
            name='vender_about',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='vender_address',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]