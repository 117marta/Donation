# Generated by Django 3.2.11 on 2022-01-30 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation_app', '0004_auto_20220130_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='date_add',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='donation',
            name='date_taken',
            field=models.DateTimeField(null=True),
        ),
    ]
