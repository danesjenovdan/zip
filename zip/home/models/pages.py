from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from .custom_blocks import (
    AwardsAndResultsBlock,
    CalendarBlock,
    ColorBackgroundWithTextAndImageBlock,
    CurrentProjectsBlock,
    GalleryBlock,
    LatestNewsBlock,
    MaterialListBlock,
    NewsletterSignupBlock,
    NewsListBlock,
    PastEventsBlock,
    PastProjectsBlock,
    PromotionBlock,
    RelatedNewsBlock,
    RichTextBlock,
    TeamBlock,
    TitleBlock,
    UpcomingEventsBlock,
)


class HomePage(Page):
    body = StreamField(
        [
            ("title_block", TitleBlock()),
            ("upcoming_events_block", UpcomingEventsBlock()),
            ("latest_news_block", LatestNewsBlock()),
            ("current_projects_block", CurrentProjectsBlock()),
            ("promotion_block", PromotionBlock()),
            ("newsletter_signup_block", NewsletterSignupBlock()),
        ],
        blank=True,
        verbose_name=_("Page body"),
    )

    parent_page_types = ["wagtailcore.Page"]
    max_count = 2

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = _("Home page")
        verbose_name_plural = _("Home pages")


class EventListPage(Page):
    body = StreamField(
        [
            ("title_block", TitleBlock()),
            ("calendar_block", CalendarBlock()),
            ("past_events_block", PastEventsBlock()),
        ],
        blank=True,
        verbose_name=_("Page body"),
    )

    parent_page_types = ["HomePage"]
    max_count = 1

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = _("Event list")
        verbose_name_plural = _("Event lists")


class EventPage(Page):
    category = models.ForeignKey(
        "EventCategory",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events",
        verbose_name=_("Category"),
    )
    start_datetime = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Start date and time"),
    )
    end_datetime = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("End date and time"),
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Location"),
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("Image"),
    )
    body = StreamField(
        [
            ("rich_text_block", RichTextBlock()),
            ("awards_and_results_block", AwardsAndResultsBlock()),
            ("gallery_block", GalleryBlock()),
            ("material_list_block", MaterialListBlock()),
        ],
        blank=True,
        verbose_name=_("Page body"),
    )

    parent_page_types = ["EventListPage"]

    content_panels = Page.content_panels + [
        FieldPanel("category"),
        FieldPanel("start_datetime"),
        FieldPanel("end_datetime"),
        FieldPanel("location"),
        FieldPanel("image"),
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")


class ProjectListPage(Page):
    current_projects = StreamField(
        [
            (
                "project",
                blocks.PageChooserBlock(
                    page_type=["home.ProjectPage"],
                    label=_("Project"),
                ),
            ),
        ],
        blank=True,
        verbose_name=_("Current projects"),
    )
    body = StreamField(
        [
            ("current_projects_block", CurrentProjectsBlock()),
            ("past_projects_block", PastProjectsBlock()),
        ],
        blank=True,
        verbose_name=_("Page body"),
    )

    parent_page_types = ["HomePage"]
    max_count = 1

    content_panels = Page.content_panels + [
        FieldPanel("current_projects"),
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = _("Project list")
        verbose_name_plural = _("Project lists")


class ProjectPage(Page):
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("Image"),
    )
    start_date = models.DateField(
        verbose_name=_("Start date"),
    )
    end_date = models.DateField(
        verbose_name=_("End date"),
    )
    body = StreamField(
        [
            ("rich_text_block", RichTextBlock()),
            ("gallery_block", GalleryBlock()),
            ("material_list_block", MaterialListBlock()),
            ("related_news_block", RelatedNewsBlock()),
        ],
        blank=True,
        verbose_name=_("Page body"),
    )

    parent_page_types = ["ProjectListPage"]

    content_panels = Page.content_panels + [
        FieldPanel("image"),
        FieldPanel("start_date"),
        FieldPanel("end_date"),
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")


class NewsListPage(Page):
    body = StreamField(
        [
            ("news_list_block", NewsListBlock()),
            ("newsletter_signup_block", NewsletterSignupBlock()),
        ],
        blank=True,
        verbose_name=_("Page body"),
    )

    parent_page_types = ["HomePage"]
    max_count = 1

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = _("News list")
        verbose_name_plural = _("News lists")


class NewsPage(Page):
    publish_datetime = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Time and date of publication"),
    )
    project = models.ForeignKey(
        "home.ProjectPage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="news",
        verbose_name=_("Project"),
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("Image"),
    )
    body = StreamField(
        [
            ("rich_text_block", RichTextBlock()),
            ("gallery_block", GalleryBlock()),
        ],
        blank=True,
        verbose_name=_("Page body"),
    )

    parent_page_types = ["NewsListPage"]

    content_panels = Page.content_panels + [
        FieldPanel("publish_datetime"),
        FieldPanel("project"),
        FieldPanel("image"),
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = _("News post")
        verbose_name_plural = _("News posts")


class AboutUsPage(Page):
    body = StreamField(
        [
            ("title_block", TitleBlock()),
            ("rich_text_block", RichTextBlock()),
            (
                "color_background_with_text_and_image_block",
                ColorBackgroundWithTextAndImageBlock(),
            ),
            ("team_block", TeamBlock()),
        ],
        blank=True,
        verbose_name=_("Page body"),
    )

    parent_page_types = ["HomePage"]
    max_count = 1

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = _("About us")
        verbose_name_plural = _("About us")


class GenericPage(Page):
    body = StreamField(
        [
            ("title_block", TitleBlock()),
            ("rich_text_block", RichTextBlock()),
            (
                "color_background_with_text_and_image_block",
                ColorBackgroundWithTextAndImageBlock(),
            ),
            ("gallery_block", GalleryBlock()),
            ("promotion_block", PromotionBlock()),
            ("newsletter_signup_block", NewsletterSignupBlock()),
        ],
        blank=True,
        verbose_name=_("Page body"),
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = _("Generic page")
        verbose_name_plural = _("Generic pages")
