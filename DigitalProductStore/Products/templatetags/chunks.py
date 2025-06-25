from django import template

register = template.Library()

@register.filter(name='chunks')
def chunks(list_data, chunk_size):
    chunked_list = []
    for i in range(0, len(list_data), chunk_size):
        chunked_list.append(list_data[i:i + chunk_size])
    return chunked_list
