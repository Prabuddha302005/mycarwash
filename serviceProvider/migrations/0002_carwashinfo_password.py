# Generated by Django 5.0.1 on 2024-07-20 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serviceProvider', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='carwashinfo',
            name='password',
            field=models.CharField(default=1, max_length=12),
            preserve_default=False,
        ),
    ]
