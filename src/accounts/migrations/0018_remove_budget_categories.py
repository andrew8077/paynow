# Generated by Django 3.2.8 on 2021-12-03 07:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_category_organization_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='budget',
            name='categories',
        ),
    ]
