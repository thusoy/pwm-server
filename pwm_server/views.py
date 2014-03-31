from . import db
from .models import Certificate, CertificateForm

from flask import Blueprint, jsonify, render_template, request, url_for
from logging import getLogger
from pwm import Domain

mod = Blueprint('views', __name__)
_logger = getLogger('pwm_server.views')

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


@mod.route('/ca/csr', methods=['POST'])
def new_csr():
    form = CertificateForm()
    if form.validate_on_submit():
        cert = Certificate()
        form.populate_obj(cert)
        db.session.add(cert)
        db.session.commit()
        _logger.info('New certificate approved')
        return jsonify({
            'msg': 'CSR accepted.',
            'href': url_for('.get_certificate', certificate_id=cert.id),
        }), 202
    else:
        _logger.warning('Got invalid CSR from %s', request.access_route)
        return jsonify({
            'msg': 'Invalid CSR',
            'errors': form.errors,
        }), 400


@mod.route('/ca/cert/<int:certificate_id>')
def get_certificate(certificate_id):
    cert = Certificate.query.get_or_404(certificate_id)
    return jsonify(cert.to_json())
