# Generated by Django 4.2.6 on 2023-10-17 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_remove_customuser_deletion_confirmation_code_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='deletion_password',
        ),
    ]
