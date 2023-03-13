# Generated by Django 4.1.7 on 2023-03-13 02:46

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0027_rename_tempupttik_upttik'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempProgramStudi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kode', models.CharField(max_length=10, unique=True)),
                ('nama', models.CharField(max_length=255)),
                ('no_sk', models.CharField(default='-', max_length=12)),
                ('tanggal_sk', models.DateField(auto_now_add=True)),
                ('tahun_operasional', models.PositiveIntegerField(default=2008, validators=[django.core.validators.MinValueValidator(2000), django.core.validators.MaxValueValidator(3000)])),
                ('jurusan', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='academic.jurusan')),
                ('program_pendidikan', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='academic.programpendidikan')),
            ],
        ),
    ]