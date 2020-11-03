import os
from flask import Flask, render_template, g
from hamlish_jinja import HamlishExtension
from werkzeug import ImmutableDict
from flask_sqlalchemy import SQLAlchemy

class FlaskWithHamlish(Flask):
    jinja_options = ImmutableDict(
        extensions=[HamlishExtension]
    )
app = FlaskWithHamlish(__name__)

db_uri = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Entry(db.Model):
    # テーブル名を定義
    __tablename__ = "db"

    # カラムを定義
    _ = db.Column(db.String(), nullable=False, primary_key=True)
    speaker = db.Column(db.String(), nullable=False, primary_key=True)
    pitch = db.Column(db.String(), nullable=False, primary_key=True)
    speed = db.Column(db.String(), nullable=False, primary_key=True)
    text = db.Column(db.String(), nullable=False, primary_key=True)
