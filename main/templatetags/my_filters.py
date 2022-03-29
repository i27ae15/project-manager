from django import template
register = template.Library()

@register.filter(name='times') 
def times(number):
    return range(int(number))


@register.filter(name='to_int')
def to_int(value):
    return int(value)