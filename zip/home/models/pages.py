from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from .custom_blocks import (
    CurrentProjectsBlock,
    LatestNewsBlock,
    NewsletterSignupBlock,
    PromotionBlock,
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

    parent_page_types = []
    max_count = 1

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = _("Home page")
        verbose_name_plural = _("Home pages")


class EventListPage(Page):
    parent_page_types = ["HomePage"]
    max_count = 1

    class Meta:
        verbose_name = _("Event list")
        verbose_name_plural = _("Event lists")


class EventPage(Page):
    parent_page_types = ["EventListPage"]

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")


class ProjectListPage(Page):
    parent_page_types = ["HomePage"]
    max_count = 1

    class Meta:
        verbose_name = _("Project list")
        verbose_name_plural = _("Project lists")


class ProjectPage(Page):
    parent_page_types = ["ProjectListPage"]

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")


class NewsListPage(Page):
    parent_page_types = ["HomePage"]
    max_count = 1

    class Meta:
        verbose_name = _("News list")
        verbose_name_plural = _("News lists")


class NewsPage(Page):
    parent_page_types = ["NewsListPage"]

    class Meta:
        verbose_name = _("News post")
        verbose_name_plural = _("News posts")


class AboutUsPage(Page):
    parent_page_types = ["HomePage"]
    max_count = 1

    class Meta:
        verbose_name = _("About us")
        verbose_name_plural = _("About us")


class GenericPage(Page):
    class Meta:
        verbose_name = _("Generic page")
        verbose_name_plural = _("Generic pages")
