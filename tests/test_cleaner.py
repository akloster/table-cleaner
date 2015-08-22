from __future__ import unicode_literals
import six

import unittest
import pandas as pd

from table_cleaner.cleaner import Cleaner, Int


class TestCleaner(unittest.TestCase):
    def test_basic(self):

        initial_df = pd.DataFrame(dict(name=["Alice", "Bob", "Wilhelm Alexander", 1, "Mary", "Andy"],
                                    email=["alice@example.com", "bob@example.com", "blub", 4, "mary@example.com",
                                    "andy k@example .com"],
                                    x=[0,3.2,"5","hello", -3,11,],
                                    y=[0.2,3.2,1.3,"hello",-3.0,11.0],
                                    active=["Y", None, "T", "false", "no", "T"]
                                    ))
        class MyCleaner(Cleaner):
            x = Int(min_value=0)

        class MyCleaner2(MyCleaner):
            y = Int(min_value=0)


        cleaner = MyCleaner2(initial_df)
