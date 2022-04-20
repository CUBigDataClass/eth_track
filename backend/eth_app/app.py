import warnings
import os
import sys

from flask import Flask
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import request


def create_app():
    app = Flask('eth_app')
    app.debug = True

    configure_blueprints(app)
   
    return app

def configure_blueprints(app):
    import eth_app.views
    app.register_blueprint(eth_app.views.api, url_prefix = "/api")

app = create_app()
