from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def parametros_url(context, **kwargs):
    """Preserva parametros da query string ao paginar."""
    request = context["request"]
    params = request.GET.copy()
    for chave, valor in kwargs.items():
        if valor is None:
            params.pop(chave, None)
        else:
            params[chave] = valor
    return params.urlencode()
