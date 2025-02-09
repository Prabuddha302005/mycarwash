# Generated by Django 5.0.1 on 2024-07-28 16:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serviceProvider', '0012_remove_service_bid_services_delete_accountverify_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Business_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carwash_name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
                ('owner_name', models.CharField(max_length=50)),
                ('sid', models.ForeignKey(db_column='sid', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
