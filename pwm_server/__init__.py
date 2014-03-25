from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_File=None):
    app = Flask(__name__)

    if config_File:
        app.config.from_pyfile(config_File)
    else:
        app.config.from_envvar('PWM_CONFIG_FILE')

    db.init_app(app)

    from . import views

    app.register_blueprint(views.mod)

    return app
