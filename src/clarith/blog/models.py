from datetime import datetime, date, timedelta
from formalchemy import (
    Column,
)
from formalchemy.fields import (
    TextAreaFieldRenderer,
)
from clarith.fa.renderers import (
    RichTextFieldRenderer,
)
from sqlalchemy import (
    Integer,
    Unicode,
    UnicodeText,
    Date,
    DateTime,
    Table,
    ForeignKey,
    BLOB,
)
from sqlalchemy.orm import (
    relationship,
    backref,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from clarith.sqla import DBSession
Base = declarative_base()


class Blog(Base):
    __tablename__ = 'Blog'
    query = DBSession.query_property()
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True)
    title = Column(UnicodeText)
    description = Column(UnicodeText)
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    @property
    def recent_entries(self, limit=10):
        return self.entries[:10]

    @property
    def entries_count(self):
        return self.entries.count()

    def add_entry(self, **kwargs):
        entry = Entry(blog=self, **kwargs)
        return entry


class Entry(Base):
    __tablename__ = 'Entry'
    query = DBSession.query_property()
    id = Column(Integer, primary_key=True)
    blog_id = Column(Integer, ForeignKey("Blog.id"))
    date = Column(Date)
    slug = Column(Unicode(255))
    title = Column(UnicodeText)
    description = Column(UnicodeText,
                         renderer=RichTextFieldRenderer)
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    blog = relationship('Blog',
                        backref=backref('entries', lazy="dynamic",
                                        order_by='desc(Entry.date)'))


class Image(Base):
    __tablename__ = 'Image'
    query = DBSession.query_property()
    id = Column(Integer, primary_key=True)
    entry_id = Column(Integer, ForeignKey("Entry.id"))
    data = Column(BLOB)
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    entry = relationship('Entry',
                         backref=backref('images', lazy="dynamic"))
