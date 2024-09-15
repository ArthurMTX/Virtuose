const expect = chai.expect;

import Websock from '../core/websock.js';
import Display from '../core/display.js';

import TightPngDecoder from '../core/decoders/tightpng.js';

import FakeWebSocket from './fake.websocket.js';

function testDecodeRect(decoder, x, y, width, height, data, display, depth) {
    let sock;
    let done = false;

    sock = new Websock;
    sock.open("ws://example.com");

    sock.on('message', () => {
        done = decoder.decodeRect(x, y, width, height, sock, display, depth);
    });

    // Empty messages are filtered at multiple layers, so we need to
    // do a direct call
    if (data.length === 0) {
        done = decoder.decodeRect(x, y, width, height, sock, display, depth);
    } else {
        sock._websocket._receiveData(new Uint8Array(data));
    }

    display.flip();

    return done;
}

describe('TightPng Decoder', function () {
    let decoder;
    let display;

    before(FakeWebSocket.replace);
    after(FakeWebSocket.restore);

    beforeEach(function () {
        decoder = new TightPngDecoder();
        display = new Display(document.createElement('canvas'));
        display.resize(4, 4);
    });

    it('should handle the TightPng encoding', async function () {
        let data = [
            // Control bytes
            0xa0, 0xb4, 0x04,
            // PNG data
            0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
            0x00, 0x00, 0x00, 0x0d, 0x49, 0x48, 0x44, 0x52,
            0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x04,
            0x08, 0x02, 0x00, 0x00, 0x00, 0x26, 0x93, 0x09,
            0x29, 0x00, 0x00, 0x01, 0x84, 0x69, 0x43, 0x43,
            0x50, 0x49, 0x43, 0x43, 0x20, 0x70, 0x72, 0x6f,
            0x66, 0x69, 0x6c, 0x65, 0x00, 0x00, 0x28, 0x91,
            0x7d, 0x91, 0x3d, 0x48, 0xc3, 0x40, 0x18, 0x86,
            0xdf, 0xa6, 0x6a, 0x45, 0x2a, 0x0e, 0x76, 0x10,
            0x71, 0x08, 0x52, 0x9d, 0x2c, 0x88, 0x8a, 0x38,
            0x6a, 0x15, 0x8a, 0x50, 0x21, 0xd4, 0x0a, 0xad,
            0x3a, 0x98, 0x5c, 0xfa, 0x07, 0x4d, 0x1a, 0x92,
            0x14, 0x17, 0x47, 0xc1, 0xb5, 0xe0, 0xe0, 0xcf,
            0x62, 0xd5, 0xc1, 0xc5, 0x59, 0x57, 0x07, 0x57,
            0x41, 0x10, 0xfc, 0x01, 0x71, 0x72, 0x74, 0x52,
            0x74, 0x91, 0x12, 0xbf, 0x4b, 0x0a, 0x2d, 0x62,
            0xbc, 0xe3, 0xb8, 0x87, 0xf7, 0xbe, 0xf7, 0xe5,
            0xee, 0x3b, 0x40, 0xa8, 0x97, 0x99, 0x66, 0x75,
            0x8c, 0x03, 0x9a, 0x6e, 0x9b, 0xa9, 0x44, 0x5c,
            0xcc, 0x64, 0x57, 0xc5, 0xd0, 0x2b, 0xba, 0x68,
            0x86, 0x31, 0x8c, 0x2e, 0x99, 0x59, 0xc6, 0x9c,
            0x24, 0x25, 0xe1, 0x3b, 0xbe, 0xee, 0x11, 0xe0,
            0xfb, 0x5d, 0x8c, 0x67, 0xf9, 0xd7, 0xfd, 0x39,
            0x7a, 0xd5, 0x9c, 0xc5, 0x80, 0x80, 0x48, 0x3c,
            0xcb, 0x0c, 0xd3, 0x26, 0xde, 0x20, 0x9e, 0xde,
            0xb4, 0x0d, 0xce, 0xfb, 0xc4, 0x11, 0x56, 0x94,
            0x55, 0xe2, 0x73, 0xe2, 0x31, 0x93, 0x2e, 0x48,
            0xfc, 0xc8, 0x75, 0xc5, 0xe3, 0x37, 0xce, 0x05,
            0x97, 0x05, 0x9e, 0x19, 0x31, 0xd3, 0xa9, 0x79,
            0xe2, 0x08, 0xb1, 0x58, 0x68, 0x63, 0xa5, 0x8d,
            0x59, 0xd1, 0xd4, 0x88, 0xa7, 0x88, 0xa3, 0xaa,
            0xa6, 0x53, 0xbe, 0x90, 0xf1, 0x58, 0xe5, 0xbc,
            0xc5, 0x59, 0x2b, 0x57, 0x59, 0xf3, 0x9e, 0xfc,
            0x85, 0xe1, 0x9c, 0xbe, 0xb2, 0xcc, 0x75, 0x5a,
            0x43, 0x48, 0x60, 0x11, 0x4b, 0x90, 0x20, 0x42,
            0x41, 0x15, 0x25, 0x94, 0x61, 0x23, 0x46, 0xbb,
            0x4e, 0x8a, 0x85, 0x14, 0x9d, 0xc7, 0x7d, 0xfc,
            0x83, 0xae, 0x5f, 0x22, 0x97, 0x42, 0xae, 0x12,
            0x18, 0x39, 0x16, 0x50, 0x81, 0x06, 0xd9, 0xf5,
            0x83, 0xff, 0xc1, 0xef, 0xde, 0x5a, 0xf9, 0xc9,
            0x09, 0x2f, 0x29, 0x1c, 0x07, 0x3a, 0x5f, 0x1c,
            0xe7, 0x63, 0x04, 0x08, 0xed, 0x02, 0x8d, 0x9a,
            0xe3, 0x7c, 0x1f, 0x3b, 0x4e, 0xe3, 0x04, 0x08,
            0x3e, 0x03, 0x57, 0x7a, 0xcb, 0x5f, 0xa9, 0x03,
            0x33, 0x9f, 0xa4, 0xd7, 0x5a, 0x5a, 0xf4, 0x08,
            0xe8, 0xdb, 0x06, 0x2e, 0xae, 0x5b, 0x9a, 0xb2,
            0x07, 0x5c, 0xee, 0x00, 0x03, 0x4f, 0x86, 0x6c,
            0xca, 0xae, 0x14, 0xa4, 0x25, 0xe4, 0xf3, 0xc0,
            0xfb, 0x19, 0x7d, 0x53, 0x16, 0xe8, 0xbf, 0x05,
            0x7a, 0xd6, 0xbc, 0xbe, 0x35, 0xcf, 0x71, 0xfa,
            0x00, 0xa4, 0xa9, 0x57, 0xc9, 0x1b, 0xe0, 0xe0,
            0x10, 0x18, 0x2d, 0x50, 0xf6, 0xba, 0xcf, 0xbb,
            0xbb, 0xdb, 0xfb, 0xf6, 0x6f, 0x4d, 0xb3, 0x7f,
            0x3f, 0x0a, 0x27, 0x72, 0x7d, 0x49, 0x29, 0x8b,
            0xbb, 0x00, 0x00, 0x00, 0x09, 0x70, 0x48, 0x59,
            0x73, 0x00, 0x00, 0x2e, 0x23, 0x00, 0x00, 0x2e,
            0x23, 0x01, 0x78, 0xa5, 0x3f, 0x76, 0x00, 0x00,
            0x00, 0x07, 0x74, 0x49, 0x4d, 0x45, 0x07, 0xe4,
            0x06, 0x06, 0x0c, 0x23, 0x1d, 0x3f, 0x9f, 0xbb,
            0x94, 0x00, 0x00, 0x00, 0x19, 0x74, 0x45, 0x58,
            0x74, 0x43, 0x6f, 0x6d, 0x6d, 0x65, 0x6e, 0x74,
            0x00, 0x43, 0x72, 0x65, 0x61, 0x74, 0x65, 0x64,
            0x20, 0x77, 0x69, 0x74, 0x68, 0x20, 0x47, 0x49,
            0x4d, 0x50, 0x57, 0x81, 0x0e, 0x17, 0x00, 0x00,
            0x00, 0x1e, 0x49, 0x44, 0x41, 0x54, 0x08, 0xd7,
            0x65, 0xc9, 0xb1, 0x0d, 0x00, 0x00, 0x08, 0x03,
            0x20, 0xea, 0xff, 0x3f, 0xd7, 0xd5, 0x44, 0x56,
            0x52, 0x90, 0xc2, 0x38, 0xa2, 0xd0, 0xbc, 0x59,
            0x8a, 0x9f, 0x04, 0x05, 0x6b, 0x38, 0x7b, 0xb2,
            0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4e, 0x44,
            0xae, 0x42, 0x60, 0x82,
        ];

        let decodeDone = testDecodeRect(decoder, 0, 0, 4, 4, data, display, 24);
        expect(decodeDone).to.be.true;

        let targetData = new Uint8Array([
            0xff, 0x00, 0x00, 255, 0xff, 0x00, 0x00, 255, 0x00, 0xff, 0x00, 255, 0x00, 0xff, 0x00, 255,
            0xff, 0x00, 0x00, 255, 0xff, 0x00, 0x00, 255, 0x00, 0xff, 0x00, 255, 0x00, 0xff, 0x00, 255,
            0x00, 0xff, 0x00, 255, 0x00, 0xff, 0x00, 255, 0xff, 0x00, 0x00, 255, 0xff, 0x00, 0x00, 255,
            0x00, 0xff, 0x00, 255, 0x00, 0xff, 0x00, 255, 0xff, 0x00, 0x00, 255, 0xff, 0x00, 0x00, 255
        ]);

        // Firefox currently has some very odd rounding bug:
        // https://bugzilla.mozilla.org/show_bug.cgi?id=1667747
        function almost(a, b) {
            let diff = Math.abs(a - b);
            return diff < 30;
        }

        await display.flush();
        expect(display).to.have.displayed(targetData, almost);
    });
});
