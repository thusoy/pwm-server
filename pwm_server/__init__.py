from flask import Flask, request, jsonify, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import argparse
import os
import hashlib
import sys

app = Flask('pwm-server')
app.config.from_envvar('PWM_CONFIG_FILE')
db = SQLAlchemy(app)


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
