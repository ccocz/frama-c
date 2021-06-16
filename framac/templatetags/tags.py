from django import template

register = template.Library()


@register.filter
def next_element(some_list, current_index):
    try:
        return some_list[int(current_index) + 1]  # access the next element
    except:
        return ''  # return empty string in case of exception


@register.filter
def previous_element(some_list, current_index):
    return some_list[int(current_index) - 1]  # access the previous element