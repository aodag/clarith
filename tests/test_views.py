import pytest
from pyramid import testing

@pytest.fixture
def config(request):
    config = testing.setUp()

    def fin():
        testing.tearDown()
    request.addfinalizer(fin)

    return config


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


class TestListEntries(object):

    @pytest.fixture
    def target(self):
        from clarith.blog.views import list_entries
        return list_entries

    @pytest.fixture
    def dummy_entries100(self):
        entries = [testing.DummyModel()
                   for i in range(100)]
        return entries

    def test_first_page(self, config, target, dummy_entries100):
        config.add_route('entries', 'testing/route/entries')
        request = testing.DummyRequest(
            matched_route=testing.DummyModel(name='entries'),
        )
        entries = dummy_entries100
        context = testing.DummyResource(
            request=request,
            blog=testing.DummyModel(
                entries=entries,
                entries_count=100,
            ),
        )
        request.context = context

        result = target(context, request)

        assert result == dict(entries=entries[:20],
                              pager='1 '
                                    '<a href="http://example.com/testing/route/entries?page=2">2</a> '
                                    '<a href="http://example.com/testing/route/entries?page=3">3</a> '
                                    '.. '
                                    '<a href="http://example.com/testing/route/entries?page=5">5</a>')

    def test_last_page(self, config, target, dummy_entries100):
        config.add_route('entries', 'testing/route/entries')
        request = testing.DummyRequest(
            matched_route=testing.DummyModel(name='entries'),
            GET=dict(page="5"),
            )
        entries = dummy_entries100
        context = testing.DummyResource(
            request=request,
            blog=testing.DummyModel(
                entries=entries,
                entries_count=100,
            ),
        )
        request.context = context

        result = target(context, request)
        assert result['entries'] == entries[-20:]
        assert result == dict(entries=entries[-20:],
                              pager='<a href="http://example.com/testing/route/entries?page=1">1</a> '
                                    '.. '
                                    '<a href="http://example.com/testing/route/entries?page=3">3</a> '
                                    '<a href="http://example.com/testing/route/entries?page=4">4</a> '
                                    '5')
