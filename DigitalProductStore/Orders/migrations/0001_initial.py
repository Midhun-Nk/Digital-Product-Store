# Generated by Django 5.2.3 on 2025-06-22 14:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Customers', '0001_initial'),
        ('Products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True)),
                ('order_status', models.IntegerField(choices=[(2, 'ORDER_PROCESSED'), (3, 'ORDER_DELIVERED'), (4, 'ORDER_REJECTED')], default=0)),
                ('delete_status', models.IntegerField(choices=[(1, 'live'), (0, 'Delete')], default=1)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='Customers.customermodels')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordered_item', to='Orders.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='added_carts', to='Products.productmodels')),
            ],
        ),
    ]
