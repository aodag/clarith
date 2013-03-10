import logging
import paginate
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from webhelpers2.text import urlify
from clarith.sqla import DBSession
from clarith.fa.views import FormView, EditFormView
from .models import Entry

logger = logging.getLogger(__name__)

@view_config(route_name="top", renderer='index.mako')
def index(context, request):
    blog = context.blog
    entries = blog.recent_entries
    return dict(blog=blog, entries=entries)


@view_config(route_name='add_entry', renderer='add_entry.mako')
class AddEntry(FormView):
    model = Entry
    db_session = DBSession

    def configure(self, fs):
        fs.configure(exclude=[fs.created, fs.updated, fs.blog])

    def validated(self, values):
        blog = self.context.blog

        if not values.get('slug'):
            values['slug'] = urlify(values['title'])

        entry = blog.add_entry(**values)

        return self.redirect_route('entry', slug=entry.slug)


    def template_values(self, values):
        blog = self.context.blog
        values.update(blog=blog)

@view_config(route_name='edit_entry', renderer='edit_entry.mako')
class EditEntry(EditFormView):
    model = Entry

    def load_model(self):
        return self.context.entry

    def configure(self, fs):
        fs.configure(exclude=[fs.created, fs.updated, fs.blog, fs.slug])

    def validated(self, values):
        blog = self.context.blog
        self.fieldset.sync()
        entry = self.fieldset.model

        return self.redirect_route('entry', slug=entry.slug)


    def template_values(self, values):
        blog = self.context.blog
        values.update(blog=blog)


@view_config(route_name="entry", request_method="GET",
             renderer='entry.mako')
def show_entry(context, request):
    entry = context.entry
    return dict(entry=entry)


@view_config(route_name='entries', renderer='entries.mako')
def list_entries(context, request):
    blog = context.blog
    page = request.GET.get('page')
    url = request.route_url(request.matched_route.name,
                            _query=dict(page='$page'),
                            **request.matchdict)
    url = url.replace("%24page", "$page")
    logger.debug('paging url = {0}'.format(url))
    page = paginate.Page(blog.entries,
                         item_count=blog.entries_count,
                         page=page)

    pager = page.pager(url=url, show_if_single_page=True)
    items = page.items

    return dict(pager=pager,
                entries=items)
