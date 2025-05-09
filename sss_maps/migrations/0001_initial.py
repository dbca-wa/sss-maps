# Generated by Django 5.0.11 on 2025-02-06 01:48

import django.core.files.storage
import sss_maps.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MapLinkedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=512, storage=django.core.files.storage.FileSystemStorage(location='/data/data/projects/sss-maps/private-media'), upload_to=sss_maps.models.upload_to_path)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
