from __future__ import unicode_literals
from table_cleaner.utils import python_2_unicode_compatible


@python_2_unicode_compatible
class Verdict(object):
    """ Base class for "Verdicts". A verdict is returned by validators
        to signal what happened to a particular cell."""
    def __init__(self, value, valid, reason="undefined", description="undefined verdict",
                 html_description=None, json_description=None):
        self.value = value
        self.valid = valid
        self.reason = reason
        self.description = description
        self.html_description = html_description
        self.json_description = json_description
    def __str__(self):
        if self.valid is True:
            return "%s is valid" % (repr(self.value),)
        elif self.valid is False:
            return "%s is invalid for reason \"%s\"" % (repr(self.value), self.reason,)
        else:
            return "warning:", repr(self.reason)
    def to_row(self):
        return dict(valid=self.valid,
                    reason=self.reason,
                    description=self.description,
                    )


class Validator(object):
    """ Abstract base class for Validators."""
    def __init__(self, *args, **kwargs):
        pass

    def validate(self, obj):
        yield Verdict(obj, True)


