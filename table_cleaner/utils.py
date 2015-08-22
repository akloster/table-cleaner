from __future__ import unicode_literals
import six


def python_2_unicode_compatible(klass):
    """
    A decorator that defines __unicode__ and __str__ methods under Python 2.
    Under Python 3 it does nothing.

    To support Python 2 and 3 with a single code base, define a __str__ method
    returning text and apply this decorator to the class.

    This was taken from the Django source code.

    """
    if six.PY2:
        if '__str__' not in klass.__dict__:
            raise ValueError("@python_2_unicode_compatible cannot be applied "
                             "to %s because it doesn't define __str__()." %
                             klass.__name__)
        klass.__unicode__ = klass.__str__
        klass.__str__ = lambda self: self.__unicode__().encode('utf-8')
    return klass

def force_text(s, encoding='utf-8', strings_only=False, errors='strict'):
    """ Forces the argument s into either a str object (Python 3) or a unicode
        object (Python 2). Taken and modified from the Django source code. """
    if isinstance(s, six.text_type):
        return s
    if not isinstance(s, six.string_types):
        if six.PY3:
            if isinstance(s, bytes):
                s = six.text_type(s, encoding, errors)
            else:
                s = six.text_type(s)
        elif hasattr(s, '__unicode__'):
            s = six.text_type(s)
        else:
            s = six.text_type(bytes(s), encoding, errors)
    else:
        try:
            s = s.decode(encoding, errors)
        except UnicodeDecodeError:
            pass
    return s
