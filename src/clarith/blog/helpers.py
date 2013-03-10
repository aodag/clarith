from webhelpers2.html import *
from webhelpers2.html.tags import *


def link_to_entry(request, entry):
    url = request.route_url("entry", slug=entry.slug)
    return link_to(entry.title, url=url)