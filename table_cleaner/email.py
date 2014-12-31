from __future__ import unicode_literals
import six

import re

from .validator import Verdict, Validator
from .utils import force_text


default_user_regex = \
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*$" \
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"$)'

# max length of the domain is 249: 254 (max email length) minus one
# period, two characters for the TLD, @ sign, & one character before @.
default_domain_regex = \
    r'(?:[A-Z0-9](?:[A-Z0-9-]{0,247}[A-Z0-9])?\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,}(?<!-))$'


class Email(Validator):
    user_regex = re.compile(default_user_regex, re.IGNORECASE)
    domain_regex = re.compile(default_domain_regex, re.IGNORECASE)

    # The whitelist makes certain domain names valid even if they are not
    # FQDNs. In particular, "mail@localhost" is a valid E-Mail address.
    domain_whitelist = ['localhost']

    def __init__(self, whitelist=None):
        if whitelist is not None:
            self.domain_whitelist = whitelist

    def validate(self, obj):
        value = force_text(obj)
        if (not value) or ('@' not in value) or (value.count('@')>1) :
            yield Verdict(obj, False, "email_without_at", \
                    "E-Mail addresses must contain one @ character.")
            if value.count("@")>1:
                yield Verdict(obj, False, "email_without_at", \
                        "E-Mail addresses must contain one @ character.")
            # Can't recover from this
            return

        user_part, domain_part = value.split("@")
        valid = True
        literal_match = self.domain_regex.match(domain_part)
        if not literal_match and not (domain_part.lower() in \
                self.domain_whitelist):
            yield Verdict(obj, False, "email_domain_name_invalid", \
                    "%s is not a valid email domain name" \
                        % (repr(domain_part),))
            valid = False

        literal_match = self.user_regex.match(user_part)
        if not literal_match:
            yield Verdict(obj, False, "email_user_name_invalid", \
                    "%s is not a valid email user name" \
                        % (repr(user_part),))
            valid = False

        if valid:
            yield Verdict(value, True)
