# Generated by Django 5.2.3

import django.db.models.deletion
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0005_homepage_body"),
    ]

    operations = [
        migrations.AddField(
            model_name="eventlistpage",
            name="body",
            field=wagtail.fields.StreamField(
                [("title_block", 4), ("calendar_block", 6), ("past_events_block", 8)],
                blank=True,
                block_lookup={
                    0: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"label": "Title", "required": False},
                    ),
                    1: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"label": "Subtitle", "required": False},
                    ),
                    2: (
                        "wagtail.blocks.RichTextBlock",
                        (),
                        {"label": "Description", "required": False},
                    ),
                    3: (
                        "wagtail.images.blocks.ImageChooserBlock",
                        (),
                        {"label": "Image", "required": False},
                    ),
                    4: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("title", 0),
                                ("subtitle", 1),
                                ("description", 2),
                                ("image", 3),
                            ]
                        ],
                        {},
                    ),
                    5: (
                        "wagtail.blocks.static_block.StaticBlock",
                        (),
                        {"admin_text": "Not implemented!", "label": "TODO"},
                    ),
                    6: ("wagtail.blocks.StructBlock", [[("todo", 5)]], {}),
                    7: ("wagtail.blocks.CharBlock", (), {"label": "Title"}),
                    8: ("wagtail.blocks.StructBlock", [[("title", 7)]], {}),
                },
                verbose_name="Page body",
            ),
        ),
        migrations.AddField(
            model_name="eventpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    ("rich_text_block", 0),
                    ("gallery_block", 2),
                    ("material_list_block", 7),
                ],
                blank=True,
                block_lookup={
                    0: ("wagtail.blocks.RichTextBlock", (), {"label": "Text"}),
                    1: (
                        "wagtail.blocks.static_block.StaticBlock",
                        (),
                        {"admin_text": "Not implemented!", "label": "TODO"},
                    ),
                    2: ("wagtail.blocks.StructBlock", [[("todo", 1)]], {}),
                    3: ("wagtail.blocks.CharBlock", (), {"label": "Title"}),
                    4: (
                        "wagtail.documents.blocks.DocumentChooserBlock",
                        (),
                        {"label": "File", "required": False},
                    ),
                    5: (
                        "wagtail.blocks.StructBlock",
                        [[("title", 3), ("file", 4)]],
                        {},
                    ),
                    6: ("wagtail.blocks.ListBlock", (5,), {"label": "Material list"}),
                    7: (
                        "wagtail.blocks.StructBlock",
                        [[("title", 3), ("material_list", 6)]],
                        {},
                    ),
                },
                verbose_name="Page body",
            ),
        ),
        migrations.AddField(
            model_name="eventpage",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="events",
                to="home.eventcategory",
                verbose_name="Category",
            ),
        ),
        migrations.AddField(
            model_name="eventpage",
            name="end_datetime",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="End date and time"
            ),
        ),
        migrations.AddField(
            model_name="eventpage",
            name="location",
            field=models.CharField(blank=True, max_length=255, verbose_name="Location"),
        ),
        migrations.AddField(
            model_name="eventpage",
            name="start_datetime",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="Start date and time"
            ),
        ),
    ]
