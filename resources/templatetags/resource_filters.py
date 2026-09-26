from django import template
from django.utils.text import slugify

register = template.Library()


@register.filter
def split(value, delimiter=','):
    """Split a string by delimiter and return a list."""
    if value:
        return [item.strip() for item in value.split(delimiter) if item.strip()]
    return []


@register.filter
def trim(value):
    """Trim whitespace from a string."""
    return value.strip() if value else ''


@register.filter
def resource_type_class(value):
    """Convert resource type to CSS class."""
    if not value:
        return 'bg-other'
    return 'bg-' + slugify(value).replace('-', '-')


@register.filter
def endswith(value, suffix):
    """Check if string ends with suffix."""
    if value is None:
        return False
    return str(value).endswith(str(suffix))