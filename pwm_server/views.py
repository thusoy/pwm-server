from . import db
from .models import Certificate, CertificateForm

from flask import Blueprint, jsonify, render_template, request, url_for
from logging import getLogger
from pwm import Domain

mod = Blueprint('views', __name__)
_logger = getLogger('pwm_server.views')

@mod.route('/')
def home():
    return render_template('main.html')


@mod.route('/domains')
def domain_search():
    domain_query = request.args.get('q')
    if not domain_query:
        return jsonify({
            'msg': 'You need to specify a query to search for',
        }), 400
    domains = db.session.query(Domain).filter(Domain.name.ilike('%%%s%%' % domain_query)).all()
    return jsonify({'domains': [
        {
        'salt': d.salt,
        'name': d.name,
        'charset': d.charset,
        'username': d.username,
        } for d in domains],
    })


@mod.route('/domains', methods=['POST'])
def new_domain():
    domain_name = request.form.get('name')
    domain_alphabet = request.form.get('alphabet')
    domain_key_length = request.form.get('length')
    if not all([domain_name, domain_alphabet, domain_key_length]):
        _logger.warning('Received invalid new domain form: name=%s, alphabet=%s, length=%s',
            domain_name, domain_alphabet, domain_key_length)
        return jsonify({
            'msg': 'name, alphabet and key_length *must* be specified!',
        }), 400
    domain_username = request.form.get('username')
    try:
        domain = Domain(name=domain_name, alphabet=domain_alphabet, key_length=domain_key_length,
            username=domain_username)
        db.session.add(domain)
        db.session.commit()
        return jsonify({
            'msg': 'New domain added succesfully',
            'domain': {
                'name': domain.name,
                'salt': domain.salt,
            }
        }), 201
    except:
        return jsonify({
            'msg': 'Did not validate',
        }), 400


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
        _logger.warning('Got invalid CSR from %s', ' -> '.join(request.access_route))
        return jsonify({
            'msg': 'Invalid CSR',
            'errors': form.errors,
        }), 400


@mod.route('/ca/cert/<int:certificate_id>')
def get_certificate(certificate_id):
    cert = Certificate.query.get_or_404(certificate_id)
    return jsonify(cert.to_json())
