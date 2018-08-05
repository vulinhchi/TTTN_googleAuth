from __future__ import print_function, unicode_literals, division, absolute_import
import datetime
import time
from mfa_ggauth import utils
from mfa_ggauth.otp import OTP

class TOTP(OTP):
    def __init__(self, *args, **kwargs):
        self.interval = kwargs.pop('interval', 30)
        super(TOTP,self).__init__(*args,**kwargs)

    def at(self, for_time, counter_offset=0):# for_time là thơời gian hiện tại
        if not isinstance(for_time, datetime.datetime):
            for_time = datetime.datetime.fromtimestamp(int(for_time))
        return self.generate_otp(self.timecode(for_time) + counter_offset)

    def now(self):
        return self.generate_otp(self.timecode(datetime.datetime.now()))

    def verify(self, otp, for_time=None, valid_window=0):
        """
        Verifies the OTP passed in against the current time OTP
        @param [String/Integer] otp the OTP to check against
        @param [Integer] valid_window extends the validity to this many counter ticks before and after the current one
        """
        if for_time is None:
            for_time = datetime.datetime.now()

        if valid_window:
            for i in range(-valid_window, valid_window + 1):
                print("i = " , i)
                print("str(self.at(for_time, i))   = ", str(self.at(for_time, i)))
                if utils.strings_equal(str(otp), str(self.at(for_time, i))):
                    return True
            return False

            print("str(self.at(for_time))  = ", str(self.at(for_time)))
        return utils.strings_equal(str(otp), str(self.at(for_time)))

    def provisioning_uri(self, name, issuer_name=None):
        """
        Returns the provisioning URI for the OTP
        This can then be encoded in a QR Code and used
        to provision the Google Authenticator app
        @param [String] name of the account
        @return [String] provisioning uri
        """
        return utils.build_uri(self.secret, name, issuer_name=issuer_name)


    def timecode(self, for_time):
        i = time.mktime(for_time.timetuple())
        # i = 1533466770.0
        print( "i = ", i)
        print("interval = ", self.interval)

        print(" timecode = ", int(i/self.interval))
        """
        i =  1533467303.0
        interval =  30
        timecode =  51115576
        """
        return int(i/self.interval)
