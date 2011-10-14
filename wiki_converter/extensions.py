from flaskext.sqlalchemy import SQLAlchemy

__all__ = [ 'db' ]

db = SQLAlchemy()
#def init_db(app):
#    db = SQLAlchemy(app)
#    return db
