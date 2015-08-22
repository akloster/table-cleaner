from __future__ import unicode_literals
import six

import unittest
import pandas as pd

from table_cleaner.table_markup import MarkupCell, MarkupFrame


class TestCellMarkup(unittest.TestCase):
    def test_basic(self):
        c = MarkupCell()
        c += "red"
        self.assertEqual(c.classes, ["red"])
        self.assertEqual(c.to_html("test"), "<td class=\"red\">test</td>")

        c += MarkupCell(classes=["yellow"])
        self.assertEqual(c.classes, ["red", "yellow"])

        c -= MarkupCell(classes=["red"])
        self.assertEqual(c.classes, ["yellow"])


        c = MarkupCell()
        c += "red"
        c += "yellow"
        self.assertEqual(c.classes, ["red", "yellow"])

        c -= "red"
        self.assertEqual(c.classes, ["yellow"])


class TestTableMarkup(unittest.TestCase):
    def setUp(self):
        self.initial_df = pd.DataFrame(dict(name=["Alice", "Bob", "Wilhelm Alexander", 1, "Mary", "Andy"],
                            email=["alice@example.com", "bob@example.com", "blub", 4, "mary@example.com",
                            "andy k@example .com"],
                            x=[0,3.2,"5","hello", -3,11,],
                            y=[0.2,3.2,1.3,"hello",-3.0,11.0],
                            active=["Y", None, "T", "false", "no", "T"]
                            ))

    def test_basic(self):
        mdf = MarkupFrame.from_dataframe(self.initial_df)
        mdf.active += "red"
        mdf.to_html()



if __name__ == '__main__':
    unittest.main()
