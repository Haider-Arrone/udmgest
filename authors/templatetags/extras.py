# seu_app/templatetags/extras.py

from django import template

register = template.Library()

@register.filter
def pluck(lista, chave):
    """
    Extrai uma lista de valores de uma lista de dicionários.

    Ex: pluck(data, 'horas') => [51.0, 30.0, ...]
    """
    return [d.get(chave) for d in lista if isinstance(d, dict)]
