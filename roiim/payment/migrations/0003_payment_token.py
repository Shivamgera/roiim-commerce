# Generated by Django 3.0.8 on 2020-07-19 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_auto_20200719_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='token',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
