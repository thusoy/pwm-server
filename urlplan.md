/
    Home page. Has a search box, where you can search for entries, click one to get data and enter passphrase.
    Also shows current devices registered.

/domains
    Search API.

/domains/<int:id>
    Get the given domain data.

/auth
    POST certificate here to get a session key.

/ca
    Status page for connected devices. From here you can approve new CSRs or revoke old certificates.

/ca/csr
    POST new CSRs here.

/ca/cert/<int:id>
    GET the given certificate.
