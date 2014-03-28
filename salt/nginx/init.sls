nginx:
    pkgrepo.managed:
        - ppa: nginx/stable

    pkg.latest:
        - require:
            - pkgrepo: nginx

    service.running:
        - require:
            - pkg: nginx
            - user: nginx
        - watch:
            - file: nginx-config

    user.present:
        - system: True


nginx-config:
    file.managed:
        - name: /etc/nginx/nginx.conf
        - source: salt://nginx/nginx.conf


nginx-sites-enabled:
    file.recurse:
        - name: /etc/nginx/sites-enabled
        - source: salt://nginx/sites-enabled
        - clean: True


nginx-ca:
    file.symlink:
        - name: /etc/nginx/ssl
        - target: /srv/ca
