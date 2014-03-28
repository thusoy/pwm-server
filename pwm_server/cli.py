from . import create_app

from pwm import PWM
import argparse
import sys

def parse_args():
    argparser = argparse.ArgumentParser(prog='pwm-server', add_help=False)
    argparser.add_argument('-d', '--debug',
        action='store_true',
        help='Run the server in the debug mode. NOT FOR PRODUCTION USE!',
    )
    argparser.add_argument('-p', '--port', metavar='<port>',
        type=int,
        default=8848,
        help='The port to run the server on',
    )
    argparser.add_argument('-h', '--host', metavar='<host>',
        help='The hostname to listen for connections to.',
    )
    argparser.add_argument('--help',
        action='store_true',
        help='Print this help message and exit',
    )
    argparser.add_argument('-c', '--config-file',
        metavar='<config-file>',
        help='Location of config file to use.',
    )
    args = argparser.parse_args()
    if args.help:
        argparser.print_help()
        sys.exit(0)
    return args


def serve():
    args = parse_args()
    app = create_app(args.config_file)
    with app.app_context():
        pwm = PWM()
        pwm.bootstrap(app.config['SQLALCHEMY_DATABASE_URI'])
    app.run(debug=args.debug, host=args.host, port=args.port)
