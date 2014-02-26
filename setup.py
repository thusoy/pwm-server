#!/usr/bin/env python
"""
    pwm-server
    ~~~~~~~~~~

    pwm-server is a backend for pwm you can (relatively) easy host yourself.

"""

from setuptools import setup, find_packages

install_requires = [
    'flask',
    'flask-sqlalchemy',
]

setup(
    name='pwm-server',
    version='0.1.0',
    author='Tarjei Husøy',
    author_email='tarjei@roms.no',
    url='https://github.com/thusoy/pwm-server',
    description="A backend for the lightweight password manager pwm",
    packages=find_packages(),
    install_requires=install_requires,
    extras_require={
        'test': ['nose', 'coverage'],
    },
    entry_points={
        'console_scripts': [
            'pwm-server = pwm_server:serve',
        ]
    },
)
