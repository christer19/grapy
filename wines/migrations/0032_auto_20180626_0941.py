# Generated by Django 2.0.2 on 2018-06-26 07:41

import django.core.validators
from django.db import migrations, models
import wines.models


class Migration(migrations.Migration):

    dependencies = [
        ('wines', '0031_auto_20180626_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendorwine',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='vendorwine',
            name='volume',
            field=models.DecimalField(decimal_places=3, default=0.75, max_digits=5, validators=[wines.models.validate_volume]),
        ),
    ]