# -*- encoding: utf-8 -*-
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from apps.services import data_service
from apps.services import selection_service
from apps.services import bokeh_service
import os


db = SQLAlchemy()
login_manager = LoginManager()


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    app.register_blueprint(data_service.data)
    app.register_blueprint(selection_service.selection)
    app.register_blueprint(bokeh_service.bokeh)
    for module_name in ('authentication', 'home'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    app.config['UPLOAD_FOLDER'] = 'apps/static/assets/data'  # Carpeta donde se guardarán los archivos
    app.config['ALLOWED_EXTENSIONS'] = {'csv'} # Extensiones permitidas
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    return app
