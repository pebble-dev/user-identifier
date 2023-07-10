import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

from . import config

BIND_APPSTORE = "appstore"
BIND_TIMELINE = "timeline"
BIND_AUTH = "auth"

db = SQLAlchemy()


class LockerEntry(db.Model):
    __tablename__ = "locker_entries"
    __bind_key__ = BIND_APPSTORE
    id = db.Column(db.Integer(), primary_key=True)
    user_token = db.Column(db.String, index=True)
    user_id = db.Column(db.Integer, index=True)


class SandboxToken(db.Model):
    __tablename__ = 'sandbox_tokens'
    __bind_key__ = BIND_TIMELINE
    token = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.Integer)
    app_uuid = db.Column(UUID(as_uuid=True))


class User(db.Model):
    __tablename__ = "users"
    __bind_key__ = BIND_AUTH
    id = db.Column(db.Integer, primary_key=True)
    subscription_expiry = db.Column(db.DateTime, nullable=True)

    @property
    def has_active_sub(self):
        return self.subscription_expiry is not None and datetime.datetime.utcnow() <= self.subscription_expiry


def init_app(app: Flask):
    app.config['SQLALCHEMY_BINDS'] = {
        BIND_APPSTORE: config.APPSTORE_DATABASE_URI,
        BIND_TIMELINE: config.TIMELINE_DATABASE_URI,
        BIND_AUTH: config.AUTH_DATABASE_URI,

    }
    db.init_app(app)
    with app.app_context():
        for engine in db.engines.values():
            engine.execution_options(postgres_readonly=True)
