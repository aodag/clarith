__author__ = 'aodag'
import pytest


class TestBlog(object):

    @pytest.fixture
    def target(self):
        from clarith.blog import models
        return models.Blog

    def test_it(self, target):
        blog = target()
        assert blog.recent_entries == []
        assert not isinstance(blog.entries, list)
        assert blog.entries_count == 0

    def test_add_entry(self, target):
        from datetime import date
        blog = target()
        result = blog.add_entry(title=u"testing entry",
                                slug=u"testing-entry-1",
                                date=date(2013, 4, 4),
                                )

        assert result in blog.entries
        assert blog.entries_count == 1
        assert blog.entries[0] == result
        assert result.blog == blog
        assert result.title == u"testing entry"
        assert result.slug == u"testing-entry-1"
        assert result.date == date(2013, 4, 4)