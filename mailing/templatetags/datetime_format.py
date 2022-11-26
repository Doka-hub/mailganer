from django import template
import pytz

register = template.Library()


@register.filter(name='tz_format')
def tz_format(datetime, tz):
    return datetime.astimezone(pytz.timezone(tz))
