from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


def db_init(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()

class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.Text, nullable=False)
    resolution = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.TIMESTAMP, nullable=False, default=datetime.datetime.utcnow)
    img = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)