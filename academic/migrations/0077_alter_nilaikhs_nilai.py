# Generated by Django 4.2.2 on 2023-07-07 14:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0076_alter_jadwalmakul_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nilaikhs',
            name='nilai',
            field=models.DecimalField(decimal_places=2, max_digits=2, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
        ),
    ]