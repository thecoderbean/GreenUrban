from django import template

register = template.Library()

@register.filter
def times(number):
    try:
        number = int(float(number))  # Convert the number to float first, then to int
        return range(number)
    except ValueError:
        return []
