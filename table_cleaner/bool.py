from __future__ import unicode_literals
import six
import numpy as np
from six.moves import filter
from .validator import Verdict, Validator

__all__ = ["Bool"]

default_true_values = [True, "True", "true", "TRUE", "On", "on", "ON",
                       "Yes", "yes", "YES", "y", "Y", "t", "T", 1, "1"]

default_false_values = [False, "False", "false", "FALSE", "Off", "off", "OFF",
                        "No", "no", "NO", "n", "N", "f", "F", 0, "0"]

default_nan_values = [None, np.nan, "nan", "NaN", "NAN"]


class Bool(Validator):
    """ The Bool validator validates boolean values from a variety of input
        types. """

    def __init__(self, true_values=default_true_values,
                       false_values=default_false_values,
                       nan_values=default_nan_values,
                       allow_nan=True,
                       default_to_nan=True):

        try:
            len(true_values)
        except TypeError:
            true_values = [true_values]

        if len(true_values) == 0:
            raise ValueError("'true_values' argument needs at least one "
                             "element.")

        try:
            len(false_values)
        except TypeError:
            false_values = [false_values]

        if len(false_values) == 0:
            raise ValueError("'false_values' argument needs at least one"
                             "element.")

        try:
            len(nan_values)
        except TypeError:
            nan_values = [nan_values]

        if len(nan_values) == 0 :
            raise ValueError("'nan_values' argument needs at least one"
                             "element.")
        if any(filter(set(true_values).__contains__, false_values)):
            raise ValueError("The lists 'true_values' and 'false_values'"
                             "must not intersect.")

        if any(filter(set(true_values).__contains__, nan_values)):
            raise ValueError("The lists 'true_values' and 'nan_values'"
                             "must not intersect.")

        if any(filter(set(false_values).__contains__, nan_values)):
            raise ValueError("The lists 'false_values' and 'nan_values'"
                             "must not intersect.")

        self.true_values = true_values
        self.false_values = false_values
        self.nan_values = nan_values

        self.allow_nan = allow_nan
        self.default_to_nan = default_to_nan

    def validate(self, obj):
        value = None
        if obj in self.true_values:
            value = True
        elif obj in self.false_values:
            value = False
        elif obj in self.nan_values:
            value = np.NaN
        else:
            # Not all types are valid inputs to np.isnan
            try:
                np.isnan(value)
                value = np.NaN
            except TypeError:
                pass

        if value is None:
            if self.default_to_nan:
                value = np.NAN
            if not self.allow_nan:
                yield Verdict(value, False, "bool nan not allowed",
                              "%s cannot be converted to True or False." %\
                                      (repr(obj),))
                return
        yield Verdict(value, True)

