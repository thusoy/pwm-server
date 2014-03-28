from . import views

from flask import Flask
from logging import getLogger
import os


_logger = getLogger('pwm_server')


def create_app(config_file=None):
    app = Flask(__name__)

    if config_file:
        config_path = os.path.join(os.getcwd(), config_file)
        _logger.debug('Loading config from %s', config_path)
        app.config.from_pyfile(config_path)
    else:
        _logger.debug('Loading config from envvar, file %s', os.environ['PWM_SERVER_CONFIG_FILE'])
        app.config.from_envvar('PWM_SERVER_CONFIG_FILE')

    app.register_blueprint(views.mod)

    return app
