# Generated by Django 2.0.2 on 2018-06-18 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wines', '0022_auto_20180615_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='rater',
            name='is_test',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vendor',
            name='is_test',
            field=models.BooleanField(default=False),
        ),
    ]
