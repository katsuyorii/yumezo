from django.template.defaulttags import register

# Создание фильтра для прохождения по циклу для закрашенных звезд
@register.filter
def range_values_star(value):
    return range(0, value)

# Создание фильтра для прохождения по циклу для не закрашенных звезд
@register.filter
def range_values_no_star(value):
    end_index = 5 - value
    return range(0, end_index)