pwm-server
==========

A lightweight backend for pwm you can host yourself.


Host it
-------

Install the script:

    $ python setup.py install

Start the server:

    $ pwm-server

Currently there can only be one user per server, but that will change...


Configuration
-------------

pwm-server in itself does not restrict access in any way, this must (for now, at least) be handled by your webserver, like Nginx or Apache.

Your free to do this however you want, but the author recommends you to not add more passwords to the mix, and rather rely on client certificates. To do this you need act as your own Certificate Authority (CA), and sign the certificates of your devices.

Once you have created your CA certificates, nginx can be configured like this to restrict access to pwm-server:

```
server {
    listen 443;
    server_name pwm.example.com;
    charset utf-8;

    ssl on;
    ssl_certificate ssl/pwm.example.com.crt;
    ssl_certificate_key ssl/example.com.key;
    ssl_client_certificate ssl/ca-chain.crt;
    ssl_verify_client on;
    ssl_verify_depth 2;


    location / {
        proxy_pass http://127.0.0.1:5000;
        include proxy_params;
    }
}

```

You can now add `https://pwm.example.com` to your pwm config, and you'll have your own, self-hosted password manager running.
