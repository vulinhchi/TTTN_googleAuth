from __future__ import print_function, unicode_literals, division, absolute_import

import unicodedata
try:
    from itertools import izip_longest
except ImportError:
    from itertools import zip_longest as izip_longest

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

def build_uri(secret, name, initial_count=None, issuer_name=None):
    is_initial_count_present = (initial_count is not None)

    otp_type = 'hotp' if is_initial_count_present else 'totp'
    base = 'otpauth://%s/' % otp_type

    if issuer_name:
        issuer_name =   quote(issuer_name)
        base += '%s:' % issuer_name

    uri = '%(base)s%(name)s?secret=%(secret)s' %{
        'name': quote(name, safe='@'),
        'secret': secret,
        'base': base,
    }

    if is_initial_count_present:
        uri += '&counter=%s' % initial_count

    if issuer_name:
        uri += '&issuer=%s' % issuer_name

    return uri

def _compare_digest(s1,s2):
    differences = 0
    for c1, c2 in izip_longest(s1,s2):
        if c1 is None or c2 is None:
            differences = 1
            continue
        differences |= ord(c1) ^ ord(c2)
    return differences == 0

try:
    from hmac import compare_digest
except ImportError:
    compare_digest = _compare_digest

def strings_equal(s1 , s2):
    try:
        s1 = unicodedata.normalize('NFKC', str(s1))
        s2 = unicodedata.normalize('NFKC', str(s2))
    except:
        s1 = unicodedata.normalize('NFKC',unicode(s1))
        s2 = unicodedata.normalize('NFKC', unicode(s2))
    return compare_digest(s1, s2)
