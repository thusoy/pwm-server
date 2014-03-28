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
        proxy_pass http://127.0.0.1:8848;
        include proxy_params;
    }
}

```

You can now add `https://pwm.example.com` to your pwm config, and you'll have your own, self-hosted password manager running.


Development
-----------

Run the unit tests to make sure you don't break anything - keep the test coverage up.

To test the integration, add pwm.local to your hosts config, and start the virtual machine with the
web servers configured:

    $ vagrant up

This should start a VM with nginx, lighttpd and apache installed, running on port 8000, 8001 and 8002, respectively. 

Make sure everything works on all the web servers, their configuration can be found in
vagrant/salt/<web-server>.

### Vagrant tips

Instead of running `vagrant provision` every time you change something in the config, instead of
re-running the entire provisioning you can rerun just the parts you are working on from inside the
VM. Log on with vagrant:vagrant (port 2222), and run `sudo salt-call state.sls <state>` to run only
one salt state.
