from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class TitleBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=False,
        label=_("Title"),
    )
    subtitle = blocks.CharBlock(
        required=False,
        label=_("Subtitle"),
    )
    description = blocks.RichTextBlock(
        required=False,
        label=_("Description"),
    )
    image = ImageChooserBlock(
        required=False,
        label=_("Image"),
    )

    class Meta:
        label = _("Title")


class UpcomingEventsBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        label=_("Title"),
    )
    link_text = blocks.CharBlock(
        required=False,
        label=_("Link text"),
    )
    page = blocks.PageChooserBlock(
        required=False,
        label=_("Page"),
    )
    displayed_items = blocks.StaticBlock(
        label=_("Displayed items"),
        admin_text=_("Next upcoming events."),
    )

    class Meta:
        label = _("Upcoming events")


class LatestNewsBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        label=_("Title"),
    )
    link_text = blocks.CharBlock(
        required=False,
        label=_("Link text"),
    )
    page = blocks.PageChooserBlock(
        required=False,
        label=_("Page"),
    )
    displayed_items = blocks.StaticBlock(
        label=_("Displayed items"),
        admin_text=_("Latest news posts."),
    )

    class Meta:
        label = _("Latest news")


class CurrentProjectsBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        label=_("Title"),
    )
    link_text = blocks.CharBlock(
        required=False,
        label=_("Link text"),
    )
    page = blocks.PageChooserBlock(
        required=False,
        label=_("Page"),
    )
    displayed_items = blocks.StaticBlock(
        label=_("Displayed items"),
        admin_text=_("Projects marked as current."),
    )

    class Meta:
        label = _("Current projects")


class PromotionBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        label=_("Title"),
    )
    image = ImageChooserBlock(
        required=False,
        label=_("Image"),
    )
    description = blocks.RichTextBlock(
        required=False,
        label=_("Description"),
    )
    link_text = blocks.CharBlock(
        required=False,
        label=_("Link text"),
    )
    url = blocks.URLBlock(
        required=False,
        label=_("Link"),
    )

    class Meta:
        label = _("Promotion")


class NewsletterSignupBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        label=_("Title"),
    )
    more_settings_elsewhere = blocks.StaticBlock(
        label=_("More settings elsewhere"),
        admin_text=_("Newsletter signup texts are managed under Footer settings."),
    )

    class Meta:
        label = _("Newsletter signup")
