from __future__ import unicode_literals
import numpy as np
from .validator import Validator, Verdict
import six

numeric_dtypes = sum([values for key, values in \
                    six.iteritems(np.sctypes)
    if key !="others"], [])

all_names = ['Numeric', 'Int', 'Int8', 'Int16', 'Int32', 'Int64', 'Float16', 'Float32', 'Float64',
           'Float128', 'Uint8', 'Uint16', 'Uint32', 'Uint64', 'Complex64',
           'Complex128', 'Complex256']

__all__ = all_names

class Numeric(Validator):
    """ Validates numeric values. This is a base class which should not be
        instantiated on its own. Every subclass needs to override the dtype
        property which controls how values are validated and the dtype of the
        validated value."""

    dtype = None

    def __init__(self, min_value=None, max_value=None):
        if self.dtype is None:
            raise ValueError("dtype property needs to be set to a particular"+
                             "numpy dtype. Probably you tried to use the"+
                             "Numeric abstract baseclass instead of one of"+
                             "its specific subclasses.")

        if not (self.dtype in numeric_dtypes):
            raise ValueError("dtype property must be set to numeric dtype. "+
                             "%s is not considered to be a numeric dtype."\
                                       % (repr(self.dtype),))
        if (max_value is not None) and (min_value is not None):
            if min_value > max_value:
                raise ValueError("max_value must be greater than or equal min_length")

        self.min_value = min_value
        self.max_value = max_value

    def validate(self, obj):
        try:
            value = self.dtype(obj)
        except (ValueError, TypeError):
            yield Verdict(obj, False, "invalid %s" % (self.dtype.__name__,),\
                    "%s cannot be converted to %s" % \
                        (repr(obj), self.dtype.__name__) )
            return

        valid = True

        if (self.min_value is not None) and (value < self.min_value):
            yield Verdict(value, False, "value too low",
                            "%i is lower than %i" % (value, self.min_value))
            valid = False
        elif (self.max_value is not None) and (value > self.max_value):
                yield Verdict(value, False, "value too high",
                              "%i is higher than %i" % (value, self.max_value))
                valid = False

        if not valid:
            return

        yield Verdict(value, True)


class Int(Numeric):
    dtype = np.int32


class Int8(Numeric):
	dtype = np.int8


class Int16(Numeric):
	dtype = np.int16


class Int32(Numeric):
	dtype = np.int32


class Int64(Numeric):
	dtype = np.int64


class Float16(Numeric):
	dtype = np.float16


class Float32(Numeric):
	dtype = np.float32


class Float64(Numeric):
	dtype = np.float64


class Float128(Numeric):
	dtype = np.float128


class Uint8(Numeric):
	dtype = np.uint8


class Uint16(Numeric):
	dtype = np.uint16


class Uint32(Numeric):
	dtype = np.uint32


class Uint64(Numeric):
	dtype = np.uint64


class Complex64(Numeric):
	dtype = np.complex64


class Complex128(Numeric):
	dtype = np.complex128


class Complex256(Numeric):
	dtype = np.complex256

