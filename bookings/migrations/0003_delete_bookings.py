# Generated by Django 5.0.1 on 2024-07-28 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_bookings_spid'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Bookings',
        ),
    ]
