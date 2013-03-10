from pyramid.config import Configurator
from pyramid.events import subscriber

@subscriber('pyramid.events.BeforeRender')
def register_helpers(event):
    from . import helpers
    event['h'] = helpers


def includeme(config):
    config.add_route('top', '/')
    config.add_route('add_entry', '/add_entry')
    config.add_route('entries', '/entries')
    config.add_route('edit_entry', '/entries/{slug}/edit')
    config.add_route('entry', '/entries/{slug}')
    config.scan()


def main(global_conf, **settings):
    config = Configurator(settings=settings,
                          root_factory='.resources.BlogResource')
    config.include(".")
    return config.make_wsgi_app()
