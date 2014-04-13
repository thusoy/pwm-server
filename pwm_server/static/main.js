(function ($, scrypt, encoding) {
    'use strict';

    var searchField = $('form.domain-search input');
    searchField.on('keyup', function () {
        $.ajax('/domains', {
            data: $('form.domain-search').serialize(),
            success: function (data) {
                var html = '<h2>Search results</h2>';
                data.domains.forEach(function (domain) {
                    html += '<div class="domain">';
                    html += '<h3>' + domain.name + '</h3>';
                    html += '<span><strong>Username: </strong>' + domain.username + '</span><br>';
                    html += '<input class="password-entry" data-salt="' + domain.salt +
                        '" data-domain="' + domain.name + '" type="password" ' +
                        'placeholder="Enter password"><br>';
                    html += 'Key: <input class="key" placeholder="Enter password to compute">';
                    html += '</div>';
                });
                $('.search-results').html(html);
                $('.password-entry').on('keyup', function (evt) {
                    var keyCodeEnter = 13;
                    if (evt.keyCode === keyCodeEnter) {
                        computePasskey(this);
                    }
                });
            }
        });
    });

    function computePasskey(el) {
        var $el = $(el);
        var masterPassword = $el.val();
        var domainName = $el.attr('data-domain');
        var salt = atob($el.attr('data-salt'));
        $el.siblings('.key').val(computeKey(domainName, masterPassword, salt));
    }

    function scrypt_hash(domain, password, salt) {
        return scrypt.crypto_scrypt(scrypt.encode_utf8(password), salt,
            Math.pow(2, 14), 8, 1, 64);
    }

})(jQuery, scrypt_module_factory(), encoding);
