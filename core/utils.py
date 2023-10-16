import math
from urllib.parse import urlencode

from django.core.paginator import Paginator
from django.template.loader import render_to_string


def set_pagination(request, items, item_numer=10):
    if not items:
        return True, "These is no items"

    params = request.GET
    item_len = len(items)
    page = int(params.get("page")) if "page" in params else 1
    pages_number = math.ceil(item_len / item_numer)

    if page > pages_number or page <= 0:
        return False, "Page not found"

    paginator = Paginator(items, item_numer)
    items = paginator.get_page(page)

    url_params = dict()
    for key in params:
        if key != 'page':
            url_params[key] = params[key]
    page_range = []
    if pages_number < 7:
        page_range += [i for i in range(1, pages_number + 1)]
    else:
        # List the displayed pages
        page_range += [1]
        from_page = min(max(page - 2, 2), pages_number - 4)
        to_page = max(min(page + 2, pages_number - 1), 5)
        if page >= 5:
            page_range += ['...']
        page_range += [i for i in range(from_page, to_page + 1)]
        if to_page < pages_number - 1:
            page_range += ['...']
        page_range += [pages_number]

    context = dict(items=items, page_range=page_range, last=pages_number, url_params=urlencode(url_params))
    items.pagination = render_to_string('includes/pagination.html', context)
    return items, {'current_page': page, 'items': item_len, 'items_on_page': item_numer}