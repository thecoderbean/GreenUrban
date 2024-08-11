# Generated by Django 5.0.6 on 2024-07-25 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retailer', '0013_product_retailer'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_boy_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(default='Order Placed', max_length=255),
        ),
    ]
