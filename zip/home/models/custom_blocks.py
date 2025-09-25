from calendar import HTMLCalendar

from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Locale

from .snippets import TeamPosition


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
        template = "home/blocks/title_block.html"


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
        page_type=["home.EventListPage"],
        label=_("Page"),
    )
    displayed_items = blocks.StaticBlock(
        label=_("Displayed items"),
        admin_text=_("Next upcoming events."),
    )

    def get_context(self, value, parent_context=None):
        from .pages import EventListPage, EventPage

        context = super().get_context(value, parent_context=parent_context)

        event_parent_page = value["page"]
        if isinstance(event_parent_page, EventListPage):
            today = timezone.now().date()
            context["events"] = (
                EventPage.objects.child_of(event_parent_page)
                .live()
                .filter(start_datetime__date__gte=today)
                .order_by("start_datetime", "id")[:3]
            )

        return context

    class Meta:
        label = _("Upcoming events")
        template = "home/blocks/upcoming_events_block.html"


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
        page_type=["home.NewsListPage"],
        label=_("Page"),
    )
    displayed_items = blocks.StaticBlock(
        label=_("Displayed items"),
        admin_text=_("Latest news posts."),
    )

    def get_context(self, value, parent_context=None):
        from .pages import NewsPage

        context = super().get_context(value, parent_context=parent_context)

        if news_parent_page := value["page"]:
            context["news_items"] = (
                NewsPage.objects.child_of(news_parent_page)
                .live()
                .order_by("-publish_datetime", "id")[:3]
            )

        return context

    class Meta:
        label = _("Latest news")
        template = "home/blocks/latest_news_block.html"


class RelatedNewsBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        label=_("Title"),
    )

    def get_context(self, value, parent_context=None):
        from .pages import NewsPage

        context = super().get_context(value, parent_context=parent_context)

        if project_page := context["page"]:
            context["news_items"] = NewsPage.objects.filter(project=project_page).live()

        return context

    class Meta:
        label = _("Related news")
        template = "home/blocks/related_news_block.html"


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
        page_type=["home.ProjectListPage"],
        label=_("Page"),
    )
    displayed_items = blocks.StaticBlock(
        label=_("Displayed items"),
        admin_text=_("Projects marked as current."),
    )

    def get_context(self, value, parent_context=None):
        from .pages import ProjectListPage, ProjectPage

        context = super().get_context(value, parent_context=parent_context)

        project_parent_page = value["page"] if value["page"] else context["page"]
        if isinstance(project_parent_page, ProjectListPage):
            today = timezone.now().date()
            context["current_projects"] = (
                ProjectPage.objects.child_of(project_parent_page)
                .live()
                .filter(start_date__lte=today)
                .filter(Q(end_date__gte=today) | Q(end_date__isnull=True))
            )

        return context

    class Meta:
        label = _("Current projects")
        template = "home/blocks/current_projects_block.html"


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
        template = "home/blocks/promotion_block.html"


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
        template = "home/blocks/newsletter_signup_block.html"


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super().__init__()

    def formatday(self, date):
        from .pages import EventPage

        v = []
        a = v.append

        events = EventPage.objects.filter(
            Q(start_datetime__date__lte=date, end_datetime__date__gte=date)
            | Q(start_datetime__date=date, end_datetime__date__isnull=True)
        )

        has_events = events.exists()
        weekday = date.weekday()
        css_class = self.cssclasses[weekday]
        if date.month != self.month:
            css_class = f"{css_class} {self.cssclass_noday}"
        if has_events:
            css_class = f"{css_class} has-events"

        a(f'<td class="{css_class}">')
        a(f'<div class="day">')
        a(f'<div class="num">{date.day}</div>')
        if has_events:
            a(f'<div class="events">')
            for event in events:
                icon_url = (
                    event.category.image.get_rendition("fill-40x40").url
                    if event.category and event.category.image
                    else ""
                )
                a(
                    f'<a class="event" href="{event.url}" title="{event.title}"><img src="{icon_url}" alt="{event.title}"></a>'
                )
            a(f"</div>")
        a(f"</div>")
        a("</td>")
        return "".join(v)

    def formatweek(self, theweek):
        s = "".join(self.formatday(date) for date in theweek)
        return f"<tr>{s}</tr>"

    def formatmonth(self):
        v = []
        a = v.append

        a(f'<table class="{self.cssclass_month}">')
        a(self.formatweekheader())
        for week in self.monthdatescalendar(self.year, self.month):
            a(self.formatweek(week))
        a("</table>")
        return "".join(v)


class CalendarBlock(blocks.StructBlock):
    displayed_items = blocks.StaticBlock(
        label=_("Displayed items"),
        admin_text=_("Calendar of events for the current month."),
    )

    def get_context(self, value, parent_context=None):
        from .pages import EventPage

        context = super().get_context(value, parent_context=parent_context)

        today = timezone.now().date()
        requested_month = context["request"].GET.get("month")
        if requested_month:
            try:
                requested_month = timezone.datetime.strptime(requested_month, "%Y-%m")
            except ValueError:
                requested_month = today
        else:
            requested_month = today
        current_month = requested_month.replace(day=1)
        previous_month = (current_month - timezone.timedelta(days=1)).replace(day=1)
        next_month = (current_month + timezone.timedelta(days=31)).replace(day=1)

        context["today"] = today
        context["current_month"] = current_month
        context["previous_month"] = previous_month
        context["next_month"] = next_month

        context["calendar"] = Calendar(
            current_month.year, current_month.month
        ).formatmonth()

        context["events"] = (
            EventPage.objects.filter(
                Q(
                    start_datetime__month=current_month.month,
                    start_datetime__year=current_month.year,
                )
                | Q(
                    end_datetime__month=current_month.month,
                    end_datetime__year=current_month.year,
                )
            )
            .live()
            .order_by("start_datetime", "id")
        )

        return context

    class Meta:
        label = _("Calendar")
        template = "home/blocks/calendar_block.html"


class PastEventsBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        label=_("Title"),
    )

    def get_context(self, value, parent_context=None):
        from .pages import EventListPage, EventPage
        from .snippets import EventCategory

        context = super().get_context(value, parent_context=parent_context)

        today = timezone.now().date()
        context["today"] = today

        event_parent_page = context["page"]
        if isinstance(event_parent_page, EventListPage):
            context["events"] = (
                EventPage.objects.child_of(event_parent_page)
                .filter(
                    Q(end_datetime__isnull=True, start_datetime__date__lt=today)
                    | Q(end_datetime__date__lt=today)
                )
                .live()
                .order_by("-start_datetime", "id")
            )

        all_events = EventPage.objects.all().specific()
        if all_events.exists():
            first_event = (
                all_events.filter(start_datetime__isnull=False)
                .order_by("start_datetime")
                .first()
            )
            last_event = (
                all_events.filter(end_datetime__isnull=False)
                .order_by("end_datetime")
                .last()
            )
            first_year = first_event.start_datetime.year if first_event else None
            last_year = last_event.end_datetime.year if last_event else None
            if first_year and last_year:
                context["years"] = list(range(last_year, first_year - 1, -1))
            elif first_year:
                context["years"] = [first_year]
            elif last_year:
                context["years"] = [last_year]
            else:
                context["years"] = []
        else:
            context["years"] = []

        context["categories"] = EventCategory.objects.all().order_by("name")

        return context

    class Meta:
        label = _("Past events")
        template = "home/blocks/past_events_block.html"


class GalleryBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        label=_("Title"),
    )
    images = blocks.ListBlock(
        ImageChooserBlock(label=_("Image")),
        label=_("Images"),
    )

    class Meta:
        label = _("Gallery")
        template = "home/blocks/gallery_block.html"


class MaterialBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        label=_("Title"),
    )
    description = blocks.RichTextBlock(
        required=False,
        label=_("Description"),
    )
    link = blocks.URLBlock(
        label=_("Link"),
    )

    class Meta:
        label = _("Material")


class MaterialListBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        label=_("Title"),
    )
    material_list = blocks.ListBlock(
        MaterialBlock(),
        label=_("Material list"),
    )

    class Meta:
        label = _("Material list")
        template = "home/blocks/material_list_block.html"


class PastProjectsBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        label=_("Title"),
    )

    def get_context(self, value, parent_context=None):
        from .pages import ProjectListPage, ProjectPage

        context = super().get_context(value, parent_context=parent_context)
        all_projects = ProjectPage.objects.none()

        project_parent_page = context["page"]
        if isinstance(project_parent_page, ProjectListPage):
            today = timezone.now().date()
            current_project_ids = (
                ProjectPage.objects.child_of(project_parent_page)
                .live()
                .filter(start_date__lte=today)
                .filter(Q(end_date__gte=today) | Q(end_date__isnull=True))
                .values_list("id", flat=True)
            )
            all_projects = (
                ProjectPage.objects.child_of(project_parent_page)
                .live()
                .exclude(id__in=current_project_ids)
                .order_by("-end_date", "id")
            )
            context["projects"] = all_projects

        if all_projects.exists():
            first_project = (
                all_projects.filter(start_date__isnull=False)
                .order_by("start_date")
                .first()
            )
            last_project = (
                all_projects.filter(end_date__isnull=False).order_by("end_date").last()
            )
            first_year = first_project.start_date.year if first_project else None
            last_year = last_project.end_date.year if last_project else None
            if first_year and last_year:
                context["years"] = list(range(last_year, first_year - 1, -1))
            elif first_year:
                context["years"] = [first_year]
            elif last_year:
                context["years"] = [last_year]
            else:
                context["years"] = []
        else:
            context["years"] = []

        return context

    class Meta:
        label = _("Past projects")
        template = "home/blocks/past_projects_block.html"


class NewsListBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        label=_("Title"),
    )

    def get_context(self, value, parent_context=None):
        from .pages import NewsPage

        context = super().get_context(value, parent_context=parent_context)

        if news_parent_page := context["page"]:
            context["news_items"] = (
                NewsPage.objects.child_of(news_parent_page)
                .live()
                .order_by("-publish_datetime", "id")
            )

        return context

    class Meta:
        label = _("News list")
        template = "home/blocks/news_list_block.html"


class ColorBackgroundWithTextAndImageBlock(blocks.StructBlock):
    color = blocks.ChoiceBlock(
        choices=[
            ("white", _("White")),
            ("light-yellow", _("Light Yellow")),
            ("yellow", _("Yellow")),
            ("light-red", _("Light Red")),
            ("red", _("Red")),
            ("light-gray", _("Light Gray")),
            ("gray", _("Gray")),
        ],
        default="white",
        label=_("Background color"),
    )
    title = blocks.CharBlock(
        required=False,
        label=_("Title"),
    )
    description = blocks.RichTextBlock(
        required=False,
        label=_("Description"),
    )
    image_position = blocks.ChoiceBlock(
        choices=[
            ("left", _("Left")),
            ("right", _("Right")),
        ],
        default="left",
        label=_("Image position"),
    )
    image = ImageChooserBlock(
        required=False,
        label=_("Image"),
    )

    class Meta:
        label = _("Color background with text and image")
        template = "home/blocks/color_background_with_text_and_image_block.html"


def get_team_positions():
    return [
        (position.id, position.name)
        for position in TeamPosition.objects.all().order_by("name")
    ]


class TeamMemberBlock(blocks.StructBlock):
    name = blocks.CharBlock(
        label=_("Name"),
    )
    position = blocks.ChoiceBlock(
        choices=get_team_positions,
        label=_("Position"),
    )
    image = ImageChooserBlock(
        required=False,
        label=_("Image"),
    )

    class Meta:
        label = _("Team member")


class TeamBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        label=_("Title"),
    )
    members = blocks.ListBlock(
        TeamMemberBlock(),
        label=_("Members"),
    )

    def get_context(self, value, parent_context=None):
        from .snippets import TeamPosition

        context = super().get_context(value, parent_context=parent_context)

        locale = Locale.get_active()
        context["positions"] = TeamPosition.objects.filter(locale=locale)

        return context

    class Meta:
        label = _("Team")
        template = "home/blocks/team_block.html"


class RichTextBlock(blocks.RichTextBlock):
    class Meta:
        label = _("Text")
        template = "home/blocks/rich_text_block.html"


class AwardsAndResultsBlock(blocks.StructBlock):
    awards_link = blocks.URLBlock(
        required=False,
        label=_("Link to awards"),
    )
    results_link = blocks.URLBlock(
        required=False,
        label=_("Link to results"),
    )

    class Meta:
        label = _("Awards and results")
        template = "home/blocks/awards_and_results_block.html"
