from __future__ import unicode_literals
import six

from table_cleaner.utils import python_2_unicode_compatible
import pandas as pd


@python_2_unicode_compatible
class MarkupCell(object):
    def __init__(self, classes=None, formatters=None):
        if classes is None:
            classes = list()

        if formatters is None:
            formatters = list()

        self.formatters = formatters
        self.classes = classes

    def to_html(self, content):
        if len(self.classes)>0:
            classes = " class=\""+" ".join(self.classes) +"\""
        else:
            classes = ""
        for formatter in self.formatters:
            content = formatter(content)
        return "<td{classes}>{content}</td>".format(classes=classes, content=content)

    def add_class(self, cls):
        return self.add_classes(cls)

    def add_classes(self, *classes):
        c = self.copy()
        c.classes += list(classes)
        return c

    def __str__(self):
        return ",".join(self.classes)

    def copy(self):
        return self.__class__(classes=list(self.classes), formatters=list(self.formatters))

    def __add__(self, other):
        if isinstance(other, MarkupCell):
            c = self.copy()
            c.classes += other.classes
            c.formatters +=other.formatters
            return c

        if isinstance(other, six.string_types):
            c = self.copy()
            c.classes = self.classes + [other]
            return c
        raise TypeError("Unsupported Types encountered when trying to add together MarkupCell classes")

    def __sub__(self, other):
        if isinstance(other, MarkupCell):
            c = self.copy()
            s = set(other.classes)
            c.classes = list([cls for cls in self.classes if cls not in s])
            c.formatters = list([f for f in other.formatters \
                    if f not in other.formatters])
            return c

        if isinstance(other, six.string_types):
            c = self.copy()
            c.classes = list(self.classes)
            c.classes.remove(other)
            return c
        raise TypeError("Unsupported Types encountered when trying to subtract MarkupCell classes from each other")


class MarkupFrame(pd.DataFrame):
    _attributes_ = ['original_data', 'classes']
    @classmethod
    def from_dataframe(cls, data, classes=None):
        instance = cls(dict([(k, [MarkupCell() for v in data[k]]) for k in data.columns]), index=data.index.copy())
        instance.original_data = data
        if classes is None:
            classes = ["markup-table"]
        instance.classes = classes
        return instance

    @classmethod
    def from_validation(cls, original, verdicts):
        mdf = cls.from_dataframe(original)
        invalid = verdicts[~verdicts.valid]
        for index, row in invalid.iterrows():
             mdf.ix[index, row.column] += "tc-cell-invalid"
        return mdf

    def to_html(self, max_rows=-1, max_cols=-1, show_dimensions=True):
        if self.shape != self.original_data.shape:
            raise ValueError("Markup DataFrame and original DataFrame do not share the same shape."\
                             "Did you modify the original DataFrame object?")
        html = "<table class=\"%s\">" % (" ".join(self.classes))
        html += "<thead>"
        html += "<th></th>"
        for column in self.columns:
            html += "<th>%s</th>" % column
        html += "</thead>"
        html += "<tbody>"
        for index, row in self.iterrows():
            html += "<tr>"
            html += "<th>%s</th>" % index
            for column in self.columns:
                html += row[column].to_html(self.original_data.ix[index, column])
            html += "</tr>"

        html += "</tbody>"
        html += "</table>"
        return html

