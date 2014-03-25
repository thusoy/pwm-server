from flask import abort, Blueprint, current_app, jsonify, render_template, request
from pwm import NoSuchDomainException, PWM

mod = Blueprint('views', __name__)

@mod.route('/')
def welcome():
    return render_template('welcome.html')


@mod.route('/get')
def main():
    pwm = PWM(database_path=current_app.config['SQLALCHEMY_DATABASE_URI'])
    domain_name = request.args.get('domain')
    if not domain_name:
        return jsonify({
            'msg': 'You need to specify a domain to retrieve the salt for',
        }), 400
    try:
        domain = pwm.get_domain(domain_name)
    except NoSuchDomainException:
        abort(404)
    return jsonify({
        'domain': domain_name,
        'salt': domain.salt,
    })
