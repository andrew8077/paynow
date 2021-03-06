# Generated by Django 3.2.8 on 2021-11-05 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20211105_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='collected_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
        ),
        migrations.AddField(
            model_name='account',
            name='expected_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
        ),
    ]
