from django import template

register = template.Library()

@register.filter
def get_dict_val(value, key_name):   
    return value[key_name] 