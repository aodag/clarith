import pytest
from pyramid import testing


class TestBlogResource(object):
    @pytest.fixture
    def target(self):
        from clarith.blog import resources
        return resources.BlogResource

    @pytest.fixture
    def models(self, request):
        from clarith.blog import models
        from clarith import sqla
        from sqlalchemy import create_engine
        engine = create_engine("sqlite:///")
        sqla.init(engine)
        models.Base.metadata.create_all(bind=engine)

        def fin():
            import transaction
            transaction.abort()
        request.addfinalizer(fin)

        return models

    @pytest.fixture
    def default_blog(self, models):
        blog = models.Blog(name=u"default")
        models.DBSession.add(blog)
        models.DBSession.flush()
        return blog

    @pytest.fixture
    def entry10(self, models, default_blog):
        entries = [models.Entry(blog=default_blog,
                                title=u"entry {0}".format(i),
                                slug=u"entry-{0}".format(i))
                   for i in range(10)]
        models.DBSession.flush()
        return entries

    def test_blog(self, target, default_blog):

        request = testing.DummyRequest()
        resource = target(request)

        assert resource.blog == default_blog

    def test_entry(self, target, entry10):
        entry = entry10[5]
        slug = entry.slug
        request = testing.DummyRequest(
            matchdict=dict(slug=slug)
        )
        resource = target(request)

        assert resource.entry == entry