pip:
    pkg.installed:
        - name: python-pip

    pip.installed:
        - upgrade: True
        - require:
            - pkg: pip


virtualenv:
    pip.installed:
        - require:
            - pip: pip


python-dev:
    pkg.installed


pyopenssl-reqs:
    pkg.installed:
        - name: libffi-dev


pwm-server-virtualenv:
    virtualenv.managed:
        - name: /srv/pwm-server/venv


pwm-server:
    pip.installed:
        - name: /vagrant
        - upgrade: True
        - bin_env: /srv/pwm-server/venv
        - require:
            - virtualenv: pwm-server-virtualenv
            - pkg: python-dev

    service.running:
        - watch:
            - pip: pwm-server
            - file: pwm-server-config
            - file: pwm-server-job


pwm-server-config:
    file.managed:
        - name: /srv/pwm-server/config.py
        - source: salt://pwm-server/config.py


pwm-server-job:
    file.managed:
        - name: /etc/init/pwm-server.conf
        - source: salt://pwm-server/pwm-server.conf
