# Generated by Django 5.2.3 on 2025-08-01 11:02

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0011_auto_20250801_1302"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventpage",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                unique=True,
                verbose_name="Unique ID (for calendar)",
            ),
        ),
    ]
