import argparse
from flask import Flask, request, jsonify, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import os
import hashlib
import sys

app = Flask('pwm-server')
app.config.from_envvar('PWM_CONFIG_FILE')
db = SQLAlchemy(app)


class DomainPassword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(30))
    salt = db.Column(db.String(128))


    def __init__(self, **kwargs):
        super(DomainPassword, self).__init__(**kwargs)
        self.new_salt()


    def new_salt(self):
        self.salt = os.urandom(32).encode('base64')


    def derive_domain_key(self, master_password):
        key_bytes = hashlib.sha1('%s:%s' % (master_password, self.domain)).digest()
        return key_bytes.encode('hex')


    def __repr__(self):
        return 'DomainPassword(domain=%s, dblt=%s)' % (self.domain, self.dblt)


@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/get')
def main():
    domain = request.args.get('domain')
    if not domain:
        return jsonify({
            'msg': 'You need to specify a domain to retrieve the salt for',
        }), 400
    domain_password = DomainPassword.query.filter_by(domain=domain).first()
    if not domain_password:
        domain_password = DomainPassword(domain=domain)
        db.session.add(domain_password)
        db.session.commit()
    return jsonify({
        'domain': domain,
        'salt': domain_password.salt,
    })


def parse_args():
    argparser = argparse.ArgumentParser(prog='pwm-server', add_help=False)
    argparser.add_argument('-d', '--debug',
        action='store_true',
        help='Run the server in the debug mode. NOT FOR PRODUCTION USE!',
    )
    argparser.add_argument('-p', '--port', metavar='<port>',
        type=int,
        help='The port to run the server on',
    )
    argparser.add_argument('-h', '--host', metavar='<host>',
        help='The hostname to listen for connections to.',
    )
    argparser.add_argument('--help',
        action='store_true',
        help='Print this help message and exit',
    )
    args = argparser.parse_args()
    if args.help:
        argparser.print_help()
        sys.exit(0)
    return args


def serve():
    db.create_all()
    args = parse_args()
    app.run(debug=args.debug, host=args.host, port=args.port)
