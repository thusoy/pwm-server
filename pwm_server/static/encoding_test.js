'use strict';

var encoding = require('./encoding.js');

exports.testCeilDiv = function (test) {
    test.expect(10);

    test.equal(encoding.ceildiv(0, 1), 0);
    test.equal(encoding.ceildiv(0, 7), 0);

    test.equal(encoding.ceildiv(1, 7), 1);
    test.equal(encoding.ceildiv(6, 7), 1);
    test.equal(encoding.ceildiv(7, 7), 1);
    test.equal(encoding.ceildiv(1, 1), 1);

    test.equal(encoding.ceildiv(8, 7), 2);
    test.equal(encoding.ceildiv(13, 7), 2);
    test.equal(encoding.ceildiv(14, 7), 2);
    test.equal(encoding.ceildiv(2, 1), 2);

    test.done();
};

exports.testCalcChunklen = function (test) {
    test.expect(4);

    test.deepEqual(encoding.calcChunklen(16), {binlen: 1, enclen: 2});
    test.deepEqual(encoding.calcChunklen(48), {binlen: 5, enclen: 7});
    test.deepEqual(encoding.calcChunklen(64), {binlen: 3, enclen: 4});
    test.deepEqual(encoding.calcChunklen(256), {binlen: 1, enclen: 1});

    test.done();
};

exports.testChunkToLong = function (test) {
    test.expect(5);

    var encoder = encoding.getEncoder((new Array(49)).join('a'));
    test.equal(encoder.chunkToLong('\0\0\0\0\xff'), 255);
    test.equal(encoder.chunkToLong('\0\0\0\xff\0'), 255 << 8);
    test.equal(encoder.chunkToLong('\0\0\xff\0\0'), 255 << 16);
    test.equal(encoder.chunkToLong('\0\xff\0\0\0'), 4278190080); // 255 << 24
    test.equal(encoder.chunkToLong('\xff\0\0\0\0'), 1095216660480); // 255 << 32

    test.done();
};
