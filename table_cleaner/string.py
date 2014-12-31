from __future__ import unicode_literals
from .validator import Validator, Verdict
from .utils import force_text


class String(object):
    """ Validates Strings. """

    def __init__(self, min_length=0, max_length=-1):
        if max_length>=0:
            if min_length>max_length:
                raise ValueError("max_length must be greater than min_length")
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, obj):
        value = force_text(obj)
        valid = True
        if (self.min_length>0) and (len(value) < self.min_length):
                yield Verdict(value, False, "too short",
                                     "%s has fewer than %i characters" \
                                         % (repr(value), self.min_length))
                valid = False
        elif (self.max_length>0) and (len(value) > self.max_length):
            yield Verdict(value, False, "too long",
                                     "%s has more than %i characters" \
                                         % (repr(value), self.max_length))
            valid = False

        if not valid:
            return

        yield Verdict(value, True)

