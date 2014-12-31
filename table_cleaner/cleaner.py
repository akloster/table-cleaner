from __future__ import unicode_literals
from .validators import *
import six

import pandas as pd


class TableCleaner(object):
    def __init__(self, row_validators, column_validators=[]):
        self.row_validators = row_validators
        self.column_validators = column_validators

    def validate(self, dataframe, verdict_counter = 0, delete=True):
        output_rows = []
        verdict_rows = []
        verdict_index = []
        for index, row in dataframe.iterrows():
            out_row = dict()
            for key in row.index.get_values():
                out_row[key] = None
            keys = []
            valid = True
            for key, validator in six.iteritems(self.row_validators):
                for verdict in validator.validate(row[key]):
                    vrow = verdict.to_row()
                    vrow["column"] = key
                    vrow["counter"] = verdict_counter
                    verdict_counter += 1
                    verdict_rows.append(vrow)
                    verdict_index.append(index)
                    value = verdict.value
                    valid &= verdict.valid
                if not valid:
                    continue
                keys.append(key)

                out_row[key] = value
            for key in set(dataframe.columns.get_values())-set(keys):
                out_row[key] = row[key]
            if valid and delete:
                output_rows.append(out_row)
        verdicts = pd.DataFrame(verdict_rows, index=verdict_index)
        return pd.DataFrame(output_rows), verdicts
