# Generated by Django 5.2.3 on 2025-07-28 09:36

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0008_aboutuspage_body_eventcategory_image_eventpage_image_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="projectpage",
            name="end_date",
            field=models.DateField(
                default=django.utils.timezone.now, verbose_name="End date"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="projectpage",
            name="start_date",
            field=models.DateField(
                default=django.utils.timezone.now, verbose_name="Start date"
            ),
            preserve_default=False,
        ),
    ]
