pwm-server
==========

A lightweight backend for [pwm] you can host yourself.

## NOTE

**This is a work in progress. If you think it looks interesting, file an issue or send a PR!**


Host it
-------

Install the script:

    $ python setup.py install

Start the server:

    $ pwm-server


Configuration
-------------

pwm-server in itself does not restrict access in any way, this must (for now, at least) be handled
by your webserver, like Nginx or Apache.

Your free to do this however you want, but the author recommends you to not add more passwords to
the mix, and rather rely on client certificates. To do this you need act as your own Certificate
Authority (CA), and sign the certificates of your devices.

Once you have created your CA certificates, nginx can be configured like this to restrict access to
pwm-server:

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

You can now add `https://pwm.example.com` to your pwm config, and you'll have your own, self-hosted
password manager running.


Development
-----------

Install the package and the test requirements:

    $ virtualenv venv
    $ . venv/bin/activate
    $ pip install -e .[test]

Keep test coverage up with unit tests, run them like this:

    $ nosetests pwm_server

To run the integration tests, which also tests the web server config and SSL handling, add
pwm.local to your hosts config, and start the virtual machine:

    $ vagrant up

This should start a VM with nginx, <del>lighttpd</del><sup>1</sup> and <del>apache</del><sup>2</sup> installed, running on
port 8000, 8001 and 8002, respectively.

Run the integration test suite against any of them like this:

    $ PWM_SERVER_TEST_URI=https://pwm.local:8000 nosetests integration_tests

Make sure everything works on all the web servers, their configuration can be found in
vagrant/salt/<web-server>.

<sup>1</sup>: We're not certain if it's possible to configure lighttpd to verify cetificates as a
self-signed CA, until that is confirmed lighttpd is put on hold.

<sup>2</sup>: Apache support will be added soon. Note that it might still work, we just haven't
tested it yet. Pull requests welcome! 

### Vagrant tips

Instead of running `vagrant provision` every time you change something in the config, instead of
re-running the entire provisioning you can rerun just the parts you are working on from inside the
VM. Log on with vagrant:vagrant (port 2222), and run `sudo salt-call state.sls <state>` to run only
one salt state.


[pwm]: https://github.com/thusoy/pwm
