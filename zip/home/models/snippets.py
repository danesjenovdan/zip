from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class EventCategory(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Name"),
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name=_("slug"),
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    panels = [
        FieldPanel("name"),
        FieldPanel("slug", read_only=True),
    ]

    def __str__(self):
        return f"{self.name} ({self.slug})"

    class Meta:
        verbose_name = _("Event Category")
        verbose_name_plural = _("Event Categories")
        ordering = ["name"]


@register_snippet
class TeamPosition(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Name"),
    )

    panels = [
        FieldPanel("name"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Team Position")
        verbose_name_plural = _("Team Positions")
        ordering = ["name"]
