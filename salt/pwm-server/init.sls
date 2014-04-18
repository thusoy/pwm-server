pip:
    pkg.installed:
        - name: python-pip

virtualenv:
    pip.installed:
        - require:
            - pkg: pip


python-dev:
    pkg.installed


pyopenssl-reqs:
    pkg.installed:
        - name: libffi-dev


pwm-server:
    virtualenv.managed:
        - name: /srv/pwm-server/venv
        - require:
            - pip: virtualenv

    pip.installed:
        - editable: {{ grains.get('source_location', '/vagrant') }}
        - upgrade: True
        - bin_env: /srv/pwm-server/venv
        - require:
            - virtualenv: pwm-server
            - pkg: python-dev
            - pkg: python-pip

    file.managed:
        - name: /srv/pwm-server/config.py
        - source: salt://pwm-server/config.py

    service.running:
        - watch:
            - pip: pwm-server
            - file: pwm-server
            - file: pwm-server-job


pwm-server-job:
    file.managed:
        - name: /etc/init/pwm-server.conf
        - source: salt://pwm-server/pwm-server.conf
