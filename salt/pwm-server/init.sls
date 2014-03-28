pwm-server-virtualenv:
    virtualenv.managed:
        - name: /srv/pwm-server/venv


pwm-server:
    pip.installed:
        - name: /vagrant
        - bin_env: /srv/pwm-server/venv
        - require:
            - virtualenv: pwm-server-virtualenv

    service.running:
        - watch:
            - file: pwm-server-job


pwm-server-config:
    file.managed:
        - name: /srv/pwm-server/config.py
        - source: salt://pwm-server/config.py


pwm-server-job:
    file.managed:
        - name: /etc/init/pwm-server.conf
        - source: salt://pwm-server/pwm-server.conf
