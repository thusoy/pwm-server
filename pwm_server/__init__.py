from . import views

from flask import Flask

def create_app(config_File=None):
    app = Flask(__name__)

    if config_File:
        app.config.from_pyfile(config_File)
    else:
        app.config.from_envvar('PWM_CONFIG_FILE')

    app.register_blueprint(views.mod)

    return app
