# Generated by Django 4.2.2 on 2023-08-01 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suggestions', '0004_message_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggestion',
            name='cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='expected_revenue',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
