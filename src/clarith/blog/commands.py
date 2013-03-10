import sys
import logging
from cliff.command import Command
from pyramid.paster import bootstrap
import locale


class CreateBlog(Command):
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(CreateBlog, self).get_parser(prog_name)
        parser.add_argument('config')
        return parser

    def take_transactional_action(self, parsed_args):
        config = parsed_args.config
        bootstrap(config)
        from .models import Blog, DBSession
        name = raw_input('name[default]:')
        if not name:
            name = u'default'
        title = raw_input('title:')
        title = title.decode(locale.getpreferredencoding())
        description = raw_input('description:')
        description = description.decode(locale.getpreferredencoding())
        blog = Blog(name=name, title=title, description=description)
        DBSession.add(blog)
        self.log.info(u"create blog {0}:{1}".format(name, title))

    def take_action(self, parsed_args):
        self.take_transactional_action(parsed_args)
        import transaction
        transaction.commit()
