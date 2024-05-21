from django.template.defaulttags import register

# Создание фильтра для склонения отзывов
@register.filter
def review_declination(value):
    value = int(value)

    if value % 10 == 1 and value % 100 != 11:
        return 'отзыв'
    elif value % 10 in [2, 3, 4] and value % 100 not in [12, 13, 14]:
        return 'отзыва'
    else:
        return 'отзывов'