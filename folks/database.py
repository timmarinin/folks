from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

database_url = os.environ.get('DATABASE_URL')

if database_url is not None:
    engine = create_engine(database_url, convert_unicode=True, echo=True) # echo=True
    db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
if database_url is not None:
    Base.query = db_session.query_property()

from sqlalchemy import event
from sqlalchemy.engine import Engine
import time
import logging

logging.basicConfig()
logger = logging.getLogger("myapp.sqltime")
logger.setLevel(logging.DEBUG)


@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement,
                          parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())
    logger.debug("Start Query: %s", statement)


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement,
                         parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop(-1)
    logger.debug("Query Complete!")
    logger.debug("Total Time: %f", total)
