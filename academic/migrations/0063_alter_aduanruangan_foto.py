# Generated by Django 4.1.7 on 2023-03-23 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0062_alter_ruangan_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aduanruangan',
            name='foto',
            field=models.ImageField(null=True, upload_to='academic/images/'),
        ),
    ]
