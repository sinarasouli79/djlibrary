# Generated by Django 4.2.4 on 2023-08-12 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_penalties_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='penalties',
            name='customer',
        ),
    ]
