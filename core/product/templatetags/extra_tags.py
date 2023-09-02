from django import template

register = template.Library()


def order_by_url_maker(full_path, order_by):
    """add order by at end of url"""

    if '&order_by' in full_path:
        order_by_index = full_path.index('&order_by')
        path = full_path[:order_by_index] + f"&order_by={order_by}"
    elif '?' in full_path:
        path = full_path + f"&order_by={order_by}"
    else:
        path = full_path + f"?&order_by={order_by}"

    return path

register.filter("order_by_url_maker", order_by_url_maker)