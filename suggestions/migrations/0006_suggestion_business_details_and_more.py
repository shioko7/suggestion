# Generated by Django 4.2.2 on 2023-08-03 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suggestions', '0005_suggestion_cost_suggestion_expected_revenue'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggestion',
            name='business_details',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='business_start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='depreciation_year1',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='depreciation_year2',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='depreciation_year3',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='disposal_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='fixed_asset_investment_year1',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='fixed_asset_investment_year2',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='fixed_asset_investment_year3',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='non_fixed_asset_investment_year1',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='non_fixed_asset_investment_year2',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='non_fixed_asset_investment_year3',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='other_expenses_year1',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='other_expenses_year2',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='other_expenses_year3',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='revenue_year1',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='revenue_year2',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='revenue_year3',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='yield_rate',
            field=models.DecimalField(blank=True, decimal_places=2, default=1.0, max_digits=4, null=True),
        ),
    ]
