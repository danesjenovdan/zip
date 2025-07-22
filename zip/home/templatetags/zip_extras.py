from django import template
from django.template.defaultfilters import date as date_filter
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.utils.translation import get_language
from wagtail.coreutils import camelcase_to_underscore
from wagtail.models import Page

from home.models.snippets import TeamPosition

register = template.Library()


@register.filter
def page_class_for_css_class(value):
    if not value or not isinstance(value, Page):
        return ""
    class_slug = camelcase_to_underscore(value.__class__.__name__).replace("_", "-")
    return f"template-{class_slug}"


@register.filter
def block_class_for_css_class(value):
    if value and value.__class__.__name__ == "RichText":
        return "template-rich-text"
    if not value or not hasattr(value, "block") or not hasattr(value.block, "name"):
        return ""
    class_slug = value.block.name.replace("_", "-")
    return f"template-{class_slug}"


@register.filter
def strip_tags_excerpt(value, words=33):
    if not value:
        return ""
    value = str(value)
    # fix for cases where HTML tags are not properly spaced
    value = value.replace("><", "> <")
    value = strip_tags(value)
    return Truncator(value).words(words)


@register.filter
def team_position_name(value):
    if value:
        if position := TeamPosition.objects.filter(id=value).first():
            return position.name
    return value


@register.filter
def debug(value):
    from pprint import pprint

    pprint(value)
    return value


DATETIME_FORMATTERS = {
    "en": {
        "SHORT_DATETIME_FORMAT_WITH_DAY": "l, j m Y, G:i",
        "SHORT_DATE_FORMAT_WITH_DAY": "l, j m Y",
        "SHORT_DATE_FORMAT": "j m Y",
        "TIME_FORMAT": "G:i",
    },
    "sl": {
        "SHORT_DATETIME_FORMAT_WITH_DAY": "l, j. n. Y, G.i",
        "SHORT_DATE_FORMAT_WITH_DAY": "l, j. n. Y",
        "SHORT_DATE_FORMAT": "j. n. Y",
        "TIME_FORMAT": "G.i",
    },
}


@register.filter(expects_localtime=True, is_safe=False)
def zip_date(value, arg=None):
    formatter = DATETIME_FORMATTERS.get(get_language(), {}).get(arg, None)
    if not formatter:
        formatter = DATETIME_FORMATTERS.get("en", {}).get(arg, None)
    if formatter:
        return date_filter(value, formatter)
    return date_filter(value, arg)
