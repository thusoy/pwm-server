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


nginx-ssl-keys:
    file.recurse:
        - name: /etc/nginx/ssl
        - source: salt://nginx/ssl
