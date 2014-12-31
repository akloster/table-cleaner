from __future__ import unicode_literals
import six
from .validator import Validator, Verdict
import table_cleaner.numeric
from table_cleaner.numeric import *
from .bool import *
from .string import String
from .regular_expression import Regex
from .email import Email


all_names = ["Verdict", "Validator", "String"]\
          + table_cleaner.numeric.all_names \
          + ["Bool", "Regex", "Email"]

__all__ = all_names

