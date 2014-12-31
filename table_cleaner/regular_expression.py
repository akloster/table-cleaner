from __future__ import unicode_literals
import six

import re

from .validator import Verdict
from .string import String
from .utils import force_text


class Regex(String):
    regex = ''
    message = "Doesn't match."
    code = 'regex_no_match'
    inverse_match = False
    flags = 0

    def __init__(self, regex=None, message=None, code=None, inverse_match=None,\
                 flags=None, min_length=0, max_length=-1):
        if regex is not None:
            self.regex = regex
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        if inverse_match is not None:
            self.inverse_match = inverse_match
        if flags is not None:
            self.flags = flags

        # regex may be passed in as string or as precompiled regular expression
        # In the latter case, setting flags to some other value probably
        # indicates an error

        if self.flags and not isinstance(self.regex, six.string_types):
            raise TypeError("If the flags are set, regex must be a regular"
                            "expression string.")

        if isinstance(self.regex, six.string_types):
            self.regex = re.compile(self.regex, self.flags)

        super(Regex, self).__init__(min_length=min_length,
                                    max_length=max_length)

    def validate(self, obj):
        value = force_text(obj)
        if not (self.inverse_match is not bool(self.regex.search(value))):
            yield Verdict(obj, False, self.code, self.message)
        else:
            yield Verdict(value, True)
