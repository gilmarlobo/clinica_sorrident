from django import template

register = template.Library()

@register.filter
def replace_comma(value):
    """ Substitui vírgula por ponto em valores numéricos """
    if isinstance(value, (int, float)):
        return str(value)
    return str(value).replace(',', '.')
