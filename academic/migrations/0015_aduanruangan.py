# Generated by Django 4.1.7 on 2023-03-06 02:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0014_ruangan'),
    ]

    operations = [
        migrations.CreateModel(
            name='AduanRuangan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', models.TextField()),
                ('status', models.CharField(choices=[('D', 'Di Tanggapi'), ('B', 'Belum Dibaca')], default='B', max_length=1)),
                ('foto', models.ImageField(upload_to='')),
                ('ruangan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.ruangan')),
            ],
        ),
    ]
