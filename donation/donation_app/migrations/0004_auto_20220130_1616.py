# Generated by Django 3.2.11 on 2022-01-30 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation_app', '0003_donation'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='is_taken',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='institution',
            name='type',
            field=models.SmallIntegerField(choices=[(1, 'Fundacja'), (2, 'Organizacja pozarządowa'), (3, 'Zbiórka lokalna')], default=1),
        ),
    ]
