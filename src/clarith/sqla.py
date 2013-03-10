from sqlalchemy import (
    engine_from_config,
)
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session,
)
from zope.sqlalchemy import ZopeTransactionExtension as _ZTE


DBSession = scoped_session(sessionmaker(extension=_ZTE()))


def includeme(config):
    engine = engine_from_config(config.registry.settings)
    init(engine)


def init(engine):
    DBSession.remove()
    DBSession.configure(bind=engine)
