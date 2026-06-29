import re

import bleach
from django import template
from django.utils.safestring import mark_safe
import markdown as md

register = template.Library()


@register.filter
def markdown(value):
    value = re.sub(r'([^\n])\n(?=[\*\+\-] )', r'\1\n\n', value)
    value = re.sub(r'([^\n])\n(?=\d+\. )', r'\1\n\n', value)
    html = md.markdown(value, extensions=['extra'])
    tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'br', 'strong', 'em', 'a',
            'ul', 'ol', 'li', 'pre', 'code', 'blockquote', 'hr', 'img', 'table',
            'thead', 'tbody', 'tr', 'th', 'td', 'dl', 'dt', 'dd']
    attrs = {'a': ['href', 'title', 'rel'], 'img': ['src', 'alt', 'title']}
    html = bleach.clean(html, tags=tags, attributes=attrs)
    return mark_safe(html)
