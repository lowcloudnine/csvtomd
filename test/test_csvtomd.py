#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test csvtomd
------------

Test scripts/functions for testing csvtomd convertion of CSV format to
markdown tables.

--------
"""
# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------


# ---- Standard libraries
from __future__ import print_function
import csv
import sys
import unittest

# ---- Custom Libraries (w/ custom path)
# Not pythonic but since a package is not needed ...
sys.path.insert(0, "../csvtomd/")
import csvtomd

# ----------------------------------------------------------------------------
# Class: TestCvsToMdMethods
# ----------------------------------------------------------------------------


class TestCvsToMdMethods(unittest.TestCase):
    """ Checks the methods of the csvtomd.py file to ensure the CSV is
    read correctly and converted to markdown correctly.

    """
    def test_default(self):
        """ Test of a plain standard table. """
        with open('input/normal.csv') as f:
            to_convert = [row for row in csv.reader(f)]
        with open('output/normal.md') as f:
            expected = f.read().strip()
        self.assertEqual(csvtomd.md_table(to_convert), expected)

    def test_jagged(self):
        """ Test of a CSV with inconsistent number of fields on each line. """
        with open('input/jagged.csv') as f:
            to_convert = [row for row in csv.reader(f)]
        with open('output/jagged.md') as f:
            expected = f.read()
        self.assertEqual(csvtomd.md_table(to_convert, padding=2), expected)

    def test_blank_lines(self):
        """ Test of a CSV with blank lines, tests both removing the blank
        lines and not removing the blank lines.

        """
        with open('input/blank_lines.csv') as f:
            to_convert = [row for row in csv.reader(f)]
        with open('output/blank_lines.md') as f:
            expected = f.read()
        self.assertEqual(csvtomd.md_table(to_convert, padding=2), expected)

    def test_remove_blank_lines(self):
        """ Test of a CSV with blank lines, tests both removing the blank
        lines and not removing the blank lines.

        """
        with open('input/blank_lines.csv') as f:
            to_convert = [row for row in csv.reader(f) if len(row) > 0]
        with open('output/remove_blank_lines.md') as f:
            expected = f.read()
        self.assertEqual(csvtomd.md_table(to_convert, padding=2), expected)

# ----------------------------------------------------------------------------
# Name
# ----------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
