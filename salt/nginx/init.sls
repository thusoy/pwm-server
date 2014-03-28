nginx:
    pkg.installed


nginx-config:
    file.managed:
        - name: /etc/nginx/nginx.conf


nginx-sites-enabled:
    file.recurse:
        - name: /etc/nginx/sites-enabled
        - source: salt://nginx/sites-enabled
        - clean: True


nginx-ca:
    file.symlink:
        - name: /etc/nginx/ssl
        - target: /srv/ca
