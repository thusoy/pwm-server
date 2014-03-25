from pwm_server import create_app

from os import path
from pwm import PWM

dev_config = path.abspath(path.join(path.dirname(__file__), 'dev_config.py'))

app = create_app(dev_config)

with app.app_context():
    pwm = PWM()
    pwm.bootstrap(app.config['SQLALCHEMY_DATABASE_URI'])

app.run(port=8848, debug=True)
