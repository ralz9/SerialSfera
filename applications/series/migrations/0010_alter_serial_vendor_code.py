# Generated by Django 4.2.6 on 2023-10-15 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0009_serial_vendor_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serial',
            name='vendor_code',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
