# Generated by Django 4.2.6 on 2023-10-16 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_customuser_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='confirmation_code',
            field=models.CharField(default=1, max_length=6),
            preserve_default=False,
        ),
    ]
