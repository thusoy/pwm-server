ca:
    file.recurse:
        - name: /srv/ca
        - source: salt://ca/files


ca-initial-serial:
     cmd.run:
        - name: echo 01 > /srv/ca/serial
        - unless: test -f /srv/ca/serial

ca-database:
    file.touch:
        - name: /srv/ca/index.txt
