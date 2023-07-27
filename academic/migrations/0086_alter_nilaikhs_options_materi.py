# Generated by Django 4.2.3 on 2023-07-22 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0085_alter_ketuajurusan_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nilaikhs',
            options={'verbose_name_plural': 'Nilai KHS'},
        ),
        migrations.CreateModel(
            name='Materi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judul', models.CharField(max_length=255)),
                ('deskripsi', models.TextField()),
                ('tanggal_unggah', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='academic/files/')),
                ('jadwal_makul', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.jadwalmakul')),
            ],
        ),
    ]
