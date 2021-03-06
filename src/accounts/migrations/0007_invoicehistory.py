# Generated by Django 3.2.8 on 2021-11-09 05:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20211105_1647'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=25, unique=True)),
                ('description', models.CharField(max_length=500)),
                ('invoice_amount', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Amount $')),
                ('date_sent', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Sent')),
            ],
            options={
                'verbose_name': 'Invoice History',
            },
        ),
    ]
