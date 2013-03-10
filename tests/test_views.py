import pytest
from pyramid import testing


class TestIndex(object):
    @pytest.fixture
    def target(self):
        from clarith.blog import views
        return views.index

    def test_it(self, target):
        entries = [testing.DummyModel()
                   for i in range(10)]
        request = testing.DummyRequest()
        context = testing.DummyResource(
            request=request,
            blog=testing.DummyModel(
                recent_entries=entries,
            )
        )
        request.context = context
        result = target(context, request)

        assert result == dict(blog=context.blog, entries=entries)


class TestAddEntry(object):
    @pytest.fixture
    def target(self):
        from clarith.blog.views import AddEntry
        return AddEntry

    @pytest.fixture
    def config(self, request):
        config = testing.setUp()

        def fin():
            testing.tearDown()
        request.addfinalizer(fin)

        return config

    def test_it(self, target, config):
        from datetime import date
        config.add_route('entry', 'testing-entry-route/{slug}')
        request = testing.DummyRequest(
            POST={
                "Entry--title": u"testing entry",
                "Entry--date__year": u"2013",
                "Entry--date__month": u"3",
                "Entry--date__day": u"31",
                "Entry--slug": u"",
                "Entry--description": u"this is testing entry",
            })

        context = testing.DummyResource(
            request=request,
            blog=testing.DummyModel(
                add_entry=lambda **kw: testing.DummyModel(**kw),
            ),
        )
        request.context = context
        result = target(context, request)()
        assert result.location == 'http://example.com/testing-entry-route/testing-entry'

    def test_get(self, target, config):
        config.add_route('entry', 'testing-entry-route/{slug}')
        request = testing.DummyRequest(POST={})

        context = testing.DummyResource(request=request, blog=testing.DummyModel())
        request.context = context
        result = target(context, request)()
        assert 'fs' in result