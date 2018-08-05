from __future__ import print_function, unicode_literals, division, absolute_import

import base64
import hashlib
import hmac


class OTP(object):
    def __init__(self, s, digits=6, digest=hashlib.sha1):
        """
        @param [String] secret in the form of base32
        @option options digits [Integer] (6)
            Number of integers in the OTP
            Google Authenticate only supports 6 currently
        @option options digest [Callable] (hashlib.sha1)
            Digest used in the HMAC
            Google Authenticate only supports 'sha1' currently
        @returns [OTP] OTP instantiation
        """
        self.digits = digits
        self.digest = digest
        self.secret = s

    def generate_otp(self, input):
        """
        @param [Integer] input the number used seed the HMAC
        Usually either the counter, or the computed integer
        based on the Unix timestamp
        """
        print("byte_secret = ",self.byte_secret())
        # byte_secret =  b'\xe7bd\x8fW\x9a0\xf5^\xc1'
        print("self.int_to_bytestring(input) = ", self.int_to_bytestring(input))
        # self.int_to_bytestring(input) =  b'\x00\x00\x00\x00\x03\x0b\xf6k'
        print("self.digest  = ", self.digest)
        # self.digest  =  <built-in function openssl_sha1>
        print("self.digits = ", self.digits) # =6
        hmac_hash = hmac.new(
            self.byte_secret(),
            self.int_to_bytestring(input),
            self.digest,
        ).digest()
        print ("hmac_hash = ", hmac_hash)
        # hmac_hash =  b'\xb4\xe4\xa7\xf2\xe1\xda+\xd4\xd4\x9f\xb3\xe3\x16\x15\xe3.\xec\x0e\xdf\x1d'
        hmac_hash = bytearray(hmac_hash)
        offset = hmac_hash[-1] & 0xf
        code = ((hmac_hash[offset] & 0x7f) << 24 |
                (hmac_hash[offset + 1] & 0xff) << 16 |
                (hmac_hash[offset + 2] & 0xff) << 8 |
                (hmac_hash[offset + 3] & 0xff))

        print(" code = " , code)
        #  code =  1099455532
        str_code = str(code % 10 ** self.digits)
        print("str_code = ", str_code)
        # str_code =  210220
        while len(str_code) < self.digits:
            str_code = '0' + str_code

        return str_code

    def byte_secret(self):
        missing_padding = len(self.secret) % 8
        print ("self.secret =  ", self.secret) # = 45RGJD2XTIYPKXWB, la secret_key hien tai cua vlc1
        print("leng = " ,len(self.secret)) # leng  = 16
        if missing_padding != 0:
            self.secret += '=' * (8 - missing_padding)
        return base64.b32decode(self.secret, casefold=True)

    @staticmethod
    def int_to_bytestring(i, padding=8):
        """
        Turns an integer to the OATH specified
        bytestring, which is fed to the HMAC
        along with the secret
        """
        result = bytearray()
        while i != 0:
            result.append(i & 0xFF)
            i >>= 8
        # It's necessary to convert the final result from bytearray to bytes because
        # the hmac functions in python 2.6 and 3.3 don't work with bytearray
        return bytes(bytearray(reversed(result)).rjust(padding, b'\0'))
