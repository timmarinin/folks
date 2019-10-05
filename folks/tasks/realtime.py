from .app import app, logger

@app.task
def notify(session_idm, msg):
