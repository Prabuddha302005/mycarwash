# Generated by Django 5.0.1 on 2024-07-27 17:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serviceProvider', '0006_remove_accountverify_services_services'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='services',
            name='spid',
        ),
        migrations.AddField(
            model_name='services',
            name='accountid',
            field=models.ForeignKey(db_column='accountid', default=1, on_delete=django.db.models.deletion.CASCADE, to='serviceProvider.accountverify'),
            preserve_default=False,
        ),
    ]
