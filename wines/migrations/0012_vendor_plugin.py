# Generated by Django 2.0.2 on 2018-06-11 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wines', '0011_wine_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='plugin',
            field=models.CharField(default='', max_length=150),
            preserve_default=False,
        ),
    ]
