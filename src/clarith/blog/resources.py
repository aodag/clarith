from pyramid.decorator import reify
from .models import (
    Blog,
    Entry,
)


class BlogResource(object):
    def __init__(self, request):
        self.request = request

    @reify
    def blog(self):
        return Blog.query.filter(Blog.name==u"default").one()

    @reify
    def entry(self):
        slug = self.request.matchdict['slug']
        return Entry.query.filter(
            Entry.slug==slug
        ).filter(
            Entry.blog_id==self.blog.id
        ).one()