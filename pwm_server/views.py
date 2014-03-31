from . import db

from flask import Blueprint, jsonify, render_template, request
from pwm import Domain

mod = Blueprint('views', __name__)

@mod.route('/')
def welcome():
    return render_template('welcome.html')


@mod.route('/domains')
def main():
    domain_name = request.args.get('q')
    if not domain_name:
        return jsonify({
            'msg': 'You need to specify a domain to retrieve the salt for',
        }), 400
    domains = db.session.query(Domain).filter(Domain.name.ilike('%%%s%%' % domain_name)).all()
    return jsonify({'domains': [
        {
        'salt': d.salt,
        'name': d.name,
        'alphabet': d.charset,
        } for d in domains],
    })
