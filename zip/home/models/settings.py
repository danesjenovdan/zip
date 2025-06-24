from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.fields import RichTextField, StreamField


@register_setting
class HeaderSettings(BaseGenericSetting):
    logo = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("Logo"),
    )
    navigation = StreamField(
        [
            (
                "page_link",
                blocks.StructBlock(
                    [
                        (
                            "title",
                            blocks.CharBlock(
                                required=True,
                                max_length=255,
                                label=_("Title"),
                            ),
                        ),
                        (
                            "page",
                            blocks.PageChooserBlock(
                                required=True,
                                label=_("Page"),
                            ),
                        ),
                    ],
                    icon="link",
                    label=_("Internal link"),
                ),
            ),
            (
                "external_link",
                blocks.StructBlock(
                    [
                        (
                            "title",
                            blocks.CharBlock(
                                required=True,
                                max_length=255,
                                label=_("Title"),
                            ),
                        ),
                        (
                            "url",
                            blocks.URLBlock(
                                required=True,
                                label=_("Link"),
                            ),
                        ),
                    ],
                    icon="link",
                    label=_("External link"),
                ),
            ),
        ],
        blank=True,
        verbose_name=_("Navigation"),
    )

    panels = [
        FieldPanel("logo"),
        FieldPanel("navigation"),
    ]

    class Meta:
        verbose_name = _("Header Settings")


class SocialMediaPlatforms(models.TextChoices):
    BLUESKY = "bluesky", "Bluesky"
    FACEBOOK = "facebook", "Facebook"
    INSTAGRAM = "instagram", "Instagram"
    LINKEDIN = "linkedin", "LinkedIn"
    MASTODON = "mastodon", "Mastodon"
    THREADS = "threads", "Threads"
    TIKTOK = "tiktok", "TikTok"
    TWITTER = "twitter", "Twitter"
    VIMEO = "vimeo", "Vimeo"
    YOUTUBE = "youtube", "YouTube"


@register_setting
class FooterSettings(BaseGenericSetting):
    about_us = RichTextField(
        blank=True,
        verbose_name=_("About us"),
    )
    social_media_links = StreamField(
        [
            (
                "social_media_link",
                blocks.StructBlock(
                    [
                        (
                            "platform",
                            blocks.ChoiceBlock(
                                required=True,
                                choices=SocialMediaPlatforms.choices,
                                label=_("Platform"),
                            ),
                        ),
                        (
                            "url",
                            blocks.URLBlock(
                                required=True,
                                label=_("Link"),
                            ),
                        ),
                    ],
                    icon="link",
                    label=_("Social media link"),
                ),
            ),
        ],
        blank=True,
        verbose_name=_("Social media links"),
    )
    email = models.EmailField(
        blank=True,
        verbose_name=_("Email"),
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("Phone"),
    )
    newsletter_signup_title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Title"),
    )
    newsletter_signup_email_label = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Email label"),
    )
    newsletter_signup_consent_label = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Consent label"),
    )
    newsletter_signup_submit_text = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Submit text"),
    )

    panels = [
        FieldPanel("about_us"),
        MultiFieldPanel(
            [
                FieldPanel("social_media_links"),
                FieldPanel("email"),
                FieldPanel("phone"),
            ],
            heading=_("Contact info"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("newsletter_signup_title"),
                FieldPanel("newsletter_signup_email_label"),
                FieldPanel("newsletter_signup_consent_label"),
                FieldPanel("newsletter_signup_submit_text"),
            ],
            heading=_("Newsletter signup"),
        ),
    ]

    class Meta:
        verbose_name = _("Footer Settings")
