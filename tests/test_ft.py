""" functional test
"""

import pytest


@pytest.fixture
def app(request):
    from clarith.blog import main
    settings = {
        "sqlalchemy.url": "sqlite:///",
        "pyramid.includes": [
            "pyramid_layout",
            "clarith.sqla",
        ],
        "mako.directories": [
            "clarith.blog:templates",
        ]
    }
    app = main({}, **settings)
    from clarith.blog import models
    from clarith.sqla import DBSession
    models.Base.metadata.create_all(bind=DBSession.bind)
    default_blog = models.Blog(name=u"default",
                               title=u"testing blog")
    from datetime import date, timedelta
    base_date = date(2013, 3, 1)
    entries = [models.Entry(blog=default_blog,
                            slug=u'entry-{0}'.format(i),
                            title=u'testing entry {0}'.format(i),
                            date=base_date+timedelta(days=i))
               for i in range(100)]
    DBSession.add(default_blog)
    DBSession.flush()
    DBSession.refresh(default_blog)

    def fin():
        import transaction
        transaction.abort()
    request.addfinalizer(fin)

    from webtest import TestApp
    app = TestApp(app)
    return app


def test_index(app):
    response = app.get('/')
    assert 'testing blog' in response
    assert 'testing blog 0' not in response
    assert 'testing entry 99' in response


def test_add_entry(app):
    response = app.get('/add_entry')
    response.form['Entry--title'] = 'testing entry'
    response.form['Entry--slug'] = ''
    response.form['Entry--date__year'] = '2013'
    response.form['Entry--date__month'] = '3'
    response.form['Entry--date__day'] = '21'
    response.form['Entry--description'] = 'this is description of testing entry'
    response = response.form.submit()

    assert response.location == 'http://localhost/entries/testing-entry'
    response = app.get(response.location)
    assert 'testing entry' in response
    assert '03/21/2013' in response.body