from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from logging import getLogger
import os
import pwm

db = SQLAlchemy()
_logger = getLogger('pwm_server')

class PWMApp(Flask):

    def bootstrap(self):
        """ Initialize database tables for both pwm_server and pwm. """
        from .models import Certificate
        with self.app_context():
            db.metadata.create_all(db.engine, tables=[Certificate.__table__, pwm.Domain.__table__])


def create_app(config_file=None):
    app = PWMApp(__name__)
    app.config['WTF_CSRF_ENABLED'] = False

    if config_file:
        config_path = os.path.join(os.getcwd(), config_file)
        _logger.debug('Loading config from %s', config_path)
    else:
        _logger.debug('Loading config from envvar, file %s', os.environ['PWM_SERVER_CONFIG_FILE'])
        config_path = os.path.join(os.getcwd(), os.environ['PWM_SERVER_CONFIG_FILE'])
    app.config.from_pyfile(config_path)

    from . import views
    app.register_blueprint(views.mod)

    db.init_app(app)

    return app
