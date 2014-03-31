from . import db

from flask.ext.wtf import Form
from OpenSSL import crypto
from wtforms import ValidationError
from wtforms_alchemy import model_form_factory
import datetime


class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    submitted_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    verified_date = db.Column(db.DateTime)
    status = db.Column(db.String(10), nullable=False, default='new')


class CertificateForm(model_form_factory(Form)):
    class Meta:
        model = Certificate
        only = (
            'content',
        )

    def validate_content(self, field):
        if field.data:
            try:
                crypto.load_certificate_request(crypto.FILETYPE_PEM, field.data)
            except crypto.Error:
                raise ValidationError("Invalid certificate request.")
