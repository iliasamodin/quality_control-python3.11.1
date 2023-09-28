# Generated by Django 4.0.6 on 2023-09-28 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ore', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concentrate',
            name='aluminum',
            field=models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='concentrate',
            name='calcium',
            field=models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='concentrate',
            name='iron',
            field=models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='concentrate',
            name='silicon',
            field=models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='concentrate',
            name='sulfur',
            field=models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=7),
        ),
    ]