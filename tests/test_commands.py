import pytest
import mock


class TestCreateBlog(object):

    @pytest.fixture
    def target(self):
        from clarith.blog.commands import create_blog
        return create_blog

    def test_default(self, target):
        mock_input = mock.Mock()
        mock_input.side_effect = ["", "testing!", "description!"]
        result = target(mock_input)

        assert result.name == u"default"
        assert result.title == u"testing!"
        assert result.description == u"description!"

    def test_it(self, target):
        mock_input = mock.Mock()
        mock_input.side_effect = ["other", "testing!", "description!"]
        result = target(mock_input)

        assert result.name == u"other"
        assert result.title == u"testing!"
        assert result.description == u"description!"