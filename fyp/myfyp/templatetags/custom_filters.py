from django import template
import hashlib
register = template.Library()

@register.filter
def star_rating(value):
    if value is None:
        return ""
    filled_stars = '★' * value
    empty_stars = '☆' * (5 - value)
    return filled_stars + empty_stars
@register.filter
def star_range(value):
    return range(value)

@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def hash_email(value):
    email_hash = hashlib.md5(value.encode('utf-8')).hexdigest()
    return email_hash

@register.filter
def get_initials(name):
    initials = ""
    name_parts = name.split()
    for part in name_parts:
        initials += part[0].upper()
    return initials