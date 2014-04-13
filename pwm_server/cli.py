from . import create_app

from pwm import PWM
import argparse
import logging
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
    argparser.add_argument('-l', '--log-file',
        metavar='<log-file>',
        help='Log to this file',
    )
    argparser.add_argument('-v', '--verbose',
        action='store_true',
        help='Increase verbosity',
    )
    args = argparser.parse_args()
    if args.help:
        argparser.print_help()
        sys.exit(0)
    return args


def serve():
    """ Entry point for the CLI.

    Bootstrap a new database first if necessary, then start the webserver.
    """
    args = parse_args()
    _init_logging(verbose=args.verbose, log_file=args.log_file)
    app = create_app(args.config_file)
    with app.app_context():
        pwm = PWM()
        pwm.bootstrap(app.config['SQLALCHEMY_DATABASE_URI'])
    app.run(debug=args.debug, host=args.host, port=args.port)


def _init_logging(verbose=False, log_file=None):
    """ Configure loggers. """
    level = logging.DEBUG if verbose else logging.WARNING
    sysout_handler = logging.StreamHandler(sys.stdout)
    sysout_handler.setLevel(level)

    pwm_logger = logging.getLogger('pwm')
    pwm_logger.setLevel(level)
    pwm_logger.addHandler(sysout_handler)
    pwm_server_logger = logging.getLogger('pwm_server')
    pwm_server_logger.setLevel(level)
    pwm_server_logger.addHandler(sysout_handler)
    if log_file:
        logfile_handler = logging.FileHandler(log_file)
        logfile_handler.setLevel(level)
        pwm_server_logger.addHandler(logfile_handler)
