# Generated by Django 3.2.8 on 2021-12-03 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20211203_0029'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='organization_name',
            field=models.CharField(default='NO ORG', max_length=75),
        ),
    ]
