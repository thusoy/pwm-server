from flask import Blueprint, jsonify, render_template, request

mod = Blueprint('views', __name__)

@mod.route('/')
def welcome():
    return render_template('welcome.html')


@mod.route('/get')
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
