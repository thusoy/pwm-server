from pwm_server import create_app

from os import path

dev_config = path.abspath(path.join(path.dirname(__file__), 'dev_config.py'))

app = create_app(dev_config)

app.run(port=8848, debug=True)
