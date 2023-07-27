# Generated by Django 4.1.7 on 2023-03-16 02:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0046_rename_tempdosen_dosen_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mahasiswa',
            name='tahun_angkatan',
            field=models.PositiveIntegerField(default=2008, validators=[django.core.validators.MinValueValidator(2008), django.core.validators.MaxValueValidator(3000)]),
            preserve_default=False,
        ),
    ]