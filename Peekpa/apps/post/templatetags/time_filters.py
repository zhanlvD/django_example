from django import template
from datetime import datetime
from django.utils.timezone import localtime

register = template.Library()

@register.filter
def data_format_y_m_d(value):
    if not isinstance(value, datetime):
        return value
    return localtime(value).strftime("%Y-%m-%d")


@register.filter
def data_format_y_m_d_h_m_s(value):
    if not isinstance(value, datetime):
        return value
    return localtime(value).strftime("%Y/%m/%d %H:%M:%S")