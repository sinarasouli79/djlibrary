# Generated by Django 4.2.4 on 2023-08-08 13:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('borrow_inventory', models.PositiveIntegerField()),
                ('buy_inventory', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Borrow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrow_date', models.DateTimeField(auto_now_add=True)),
                ('expected_return_date', models.DateTimeField()),
                ('actual_return_date', models.DateTimeField(blank=True, null=True)),
                ('book', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='library.book')),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('borrow_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('borrow_limit', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, max_digits=5)),
                ('is_ban', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Penalties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('borrow', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='library.borrow')),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='library.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Librarian',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='borrow',
            name='customer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='library.customer'),
        ),
        migrations.AddField(
            model_name='book',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='library.collection'),
        ),
    ]
