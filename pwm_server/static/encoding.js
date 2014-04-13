/* exported encoding */

/*
* Javascript port of https://github.com/thusoy/pwm/blob/master/pwm/encoding.py
*/

var encoding = (function () {
    'use strict';

    /*
    * Integer ceilin division.
    */
    function ceildiv(dividend, divisor) {
        return Math.floor((dividend + divisor - 1) / divisor);
    }

    /*
    * Compute the ideal conversion ratio for the given alphabet.
    * A ratio is considered ideal when the number of bits in one output encoding chunk that don't
    * add up to one input encoding chunk is minimal.
    */
    function calcChunklen(alphabetLength) {
        var minimal = {};
        for (var i = 1; i < 7; i++) {
            var enclen = i*8 / (Math.log(alphabetLength) / Math.log(2));
            if (typeof(minimal.enclen) === 'undefined' || enclen % 1 < minimal.enclen % 1) {
                minimal.binlen = i;
                minimal.enclen = enclen;
            }
        }
        return {binlen: minimal.binlen, enclen: Math.floor(minimal.enclen)};
    }

    function getEncoder(alphabet) {
        var encoder = {};
        encoder.alphabet = alphabet;
        encoder.chunklen = calcChunklen(alphabet.length);

        /*
        * Encode the bytes from the scrypt hash with the encoders alphabet, limited to the given
        * length.
        */
        encoder.encode = function (bytes, length) {
            // TBD
        };


        /*
        * Get a chunk from the input data, convert it to a number and encode that number.
        */
        encoder.encodeChunk = function (data, index) {
            // TBD
        };


        /*
        * Encode an integer of 8*this.chunklen.binlen bits using the specified alphabet.
        */
        encoder.encodeLong = function (val) {
            // TBD
        };


        /*
        * Parse a chunk of bytes to integer, using big-endian representation.
        */
        encoder.chunkToLong = function (chunk) {
            var sum = 0;
            for (var i = 0; i < this.chunklen.binlen; i++) {
                sum += Math.pow(256, this.chunklen.binlen - 1 - i)*chunk[i];
            }
            return sum;
        };


        /*
        * Partition the data into chunks and retrieve the chunk at the given index.
        */
        encoder.getChunk = function (data, index) {
            // TBD
        };

        return encoder;
    }

    return {
        'getEncoder': getEncoder,
        'ceildiv': ceildiv,
        'calcChunklen': calcChunklen,
    };
})();


// Expose the module for a node environment (like nodeunit tests)
if (typeof module !== 'undefined') {
    module.exports = encoding;
}
