import warnings
import os
import sys

from eth_app.db import get_db

from flask import Flask
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import request
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask('eth_app')
    app.debug = True

    configure_blueprints(app)
    db = configure_db(app)
   
    return app


def configure_blueprints(app):
    import eth_app.views
    app.register_blueprint(eth_app.views.api, url_prefix = "/api")

def configure_db(app):
    app.config.from_mapping(
            SQLALCHEMY_DATABASE_URI="sqlite:///site.db",
            DATABASE=os.path.join(app.instance_path, "eth_app.sqlite"),
            DEBUG=True
        )
    db = SQLAlchemy(app)
    return db

class EthItem(db.Model):
