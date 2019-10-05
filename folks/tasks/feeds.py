from .celery import app, logger
import models
import database
import requests
from schema import post_schema

@app.task
def notify_readers(writer_feed_id, post_id):
    readers = database.db_session.query(models.ReaderFeed).filter(models.WriterFeed.id == writer_feed_id).all()
    post = database.db_session.query(models.Post).filter_by(id=post_id).first()
    for reader in readers:
        req = dict(token='HELLO', post=post_schema.dump(post), reader_feed=reader.id)
        requests.post('http://localhost:3000/server-side-api', json=req)