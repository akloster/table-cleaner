from __future__ import unicode_literals
from .validators import *
import six

import pandas as pd

class CleanerMetaclass(type):
    def __init__(cls, name, bases, nmspc):
        super(CleanerMetaclass, cls).__init__(name, bases, nmspc)
        if not hasattr(cls, "_fields"):
            cls._fields = {}
        else:
            cls._fields = cls._fields.copy()

        for k,v in nmspc.items():
            if k in ['__init__','__qualname__', '__module__']:
                continue
            cls._fields[k] = v


class Cleaner(six.with_metaclass(CleanerMetaclass, object)):
    def __init__(self, original, verdict_counter=0):
        output_rows = []
        verdict_rows = []
        verdict_index = []
        self.original = original

        for index, row in self.original.iterrows():
            out_row = dict()
            for key in row.index.get_values():
                out_row[key] = None
            keys = []
            valid = True
            for key, validator in six.iteritems(self._fields):
                for verdict in validator.validate(row[key]):
                    vrow = verdict.to_row()
                    vrow["column"] = key
                    vrow["counter"] = verdict_counter
                    verdict_counter += 1
                    verdict_rows.append(vrow)
                    verdict_index.append(index)
                    value = verdict.value
                    valid &= verdict.valid
                out_row[key] = value
                if not valid:
                    continue
                keys.append(key)

            for key in set(self.original.columns.get_values())-set(keys):
                out_row[key] = row[key]
            if valid:
                output_rows.append(out_row)
        self.verdicts = pd.DataFrame(verdict_rows, index=verdict_index)
        self.cleaned = pd.DataFrame(output_rows)


