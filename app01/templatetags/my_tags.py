from django import template

register = template.Library()


@register.filter
def int_to_list(num: int):
    return list(range(1, num + 1))
