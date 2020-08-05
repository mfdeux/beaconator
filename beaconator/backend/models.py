import datetime
import uuid
from sqlite3 import Connection as SQLite3Connection

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import backref, relationship

from .database import Base


def make_uuid():
    return str(uuid.uuid4())


# https://stackoverflow.com/questions/57726047/sqlalchemy-expression-language-and-sqlites-on-delete-cascade
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


class GACode(Base):
    __tablename__ = "ga_codes"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
    name = Column(String, index=True, nullable=True)
    code = Column(String, index=True)
    active = Column(Boolean, default=True)


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
    name = Column(String, index=True)
    code = Column(String, index=True, default=make_uuid)
    image = Column(String, index=True)
    ga_code_id = Column(Integer, ForeignKey("ga_codes.id", ondelete="CASCADE"))
    ga_code = relationship(
        "GACode", backref=backref("properties", passive_deletes=True)
    )
    extra_params = Column(String, nullable=True)
    active = Column(Boolean, default=True)
