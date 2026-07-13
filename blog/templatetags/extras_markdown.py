import bleach
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def markdown(valor):
    return mark_safe(valor)


@register.filter
def sanitize(valor):
    tags = bleach.sanitizer.ALLOWED_TAGS + [
        "div", "span", "h1", "h2", "h3", "h4", "h5", "h6",
        "img", "table", "thead", "tbody", "tr", "th", "td",
        "pre", "code", "blockquote", "hr", "br", "p",
        "ul", "ol", "li", "dl", "dt", "dd",
        "strong", "em", "a", "b", "i", "u", "s",
    ]
    attrs = {
        "*": ["class", "id", "style"],
        "a": ["href", "title", "rel"],
        "img": ["src", "alt", "title"],
    }
    html = bleach.clean(valor, tags=tags, attributes=attrs)
    return mark_safe(html)
