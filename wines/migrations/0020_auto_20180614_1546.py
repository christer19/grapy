# Generated by Django 2.0.2 on 2018-06-14 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wines', '0019_rater_limit'),
    ]

    operations = [
        migrations.AddField(
            model_name='rater',
            name='plugin',
            field=models.CharField(default='', max_length=150),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='winerating',
            unique_together={('wine', 'rater')},
        ),
    ]
