# Generated by Django 4.2.4 on 2023-08-11 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_alter_borrow_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='actual_return_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='borrow',
            name='borrow_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='borrow',
            name='expected_return_date',
            field=models.DateField(),
        ),
    ]