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


def create_app():
    app = Flask('eth_app')

    configure_app(app)
    configure_dirs(app)
    configure_logging(app)
    configure_app_root(app)
    configure_blueprints(app)
    configure_db(app)
    configure_errorhandlers(app)

    return app

def configure_app(app):
    print("Configuring App")

def configure_dirs(app):
    print("Configuring directories")

def configure_logging(app):
    print("Configuring logging")

def configure_app_root(app):
    print("Configuring root")

def configure_errorhandlers(app):
    print("Configuring errors")

def configure_blueprints(app):
    import eth_app.views
    app.register_blueprint(eth_app.views.api, url_prefix = "/api")

def configure_db(app):
    print("Configuring db")
    app.config.from_mapping(
            DATABASE=os.path.join(app.instance_path, "eth_app.sqlite"),
        )

