#!/usr/bin/env python
# encoding: utf-8
"""
Unit tests for utils.py
"""
from __future__ import print_function, unicode_literals
import unittest

import utils


class TestClassifiersSupport(unittest.TestCase):
    def test_has_support(self):
        # Arrange
        classifiers = [
            "Programming Language :: Python",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
        ]

        # Act
        has_support = utils.classifiers_support(classifiers, "2.6")

        # Assert
        self.assertEqual(has_support, "yes")

    def test_no_support_but_others_are(self):
        # Arrange
        classifiers = [
            "Programming Language :: Python",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
        ]

        # Act
        has_support = utils.classifiers_support(classifiers, "2.6")

        # Assert
        self.assertEqual(has_support, "no")

    def test_no_support_but_other_2x_are(self):
        # Arrange
        classifiers = [
            "Programming Language :: Python",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.7",
        ]

        # Act
        has_support = utils.classifiers_support(classifiers, "2.6")

        # Assert
        self.assertEqual(has_support, "no")

    def test_no_support_but_other_3x_are(self):
        # Arrange
        classifiers = [
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
        ]

        # Act
        has_support = utils.classifiers_support(classifiers, "2.6")

        # Assert
        self.assertEqual(has_support, "maybe")

    def test_maybe_support_or_any_major_minor(self):
        # Arrange
        # No major.minor classifiers
        classifiers = [
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
        ]

        # Act
        has_support = utils.classifiers_support(classifiers, "2.6")

        # Assert
        self.assertEqual(has_support, "maybe")

    def test_maybe_support_for_empty(self):
        # Arrange
        # No classifiers
        classifiers = []

        # Act
        has_support = utils.classifiers_support(classifiers, "2.6")

        # Assert
        self.assertEqual(has_support, "maybe")

    def test_maybe_support_for_3x(self):
        # Arrange
        # We have major but no major.minor
        classifiers = [
            "Programming Language :: Python :: 2.4",
            "Programming Language :: Python :: 2.5",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
        ]

        # Act
        has_support = utils.classifiers_support(classifiers, "3.4")

        # Assert
        self.assertEqual(has_support, "maybe")

    def test_maybe_support_for_2x(self):
        # Arrange
        # We have major but no major.minor
        classifiers = [
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
        ]

        # Act
        has_support = utils.classifiers_support(classifiers, "2.6")

        # Assert
        self.assertEqual(has_support, "maybe")


class TestRequiresPythonSupports(unittest.TestCase):
    def test_has_support(self):
        # Arrange
        python_requires = ">=2.6, !=3.0.*, !=3.1.*, !=3.2.*"

        # Act
        has_support = utils.requires_python_supports(python_requires, "2.6")

        # Assert
        self.assertEqual(has_support, "yes")

    def test_no_support_but_others_are(self):
        # Arrange
        python_requires = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*"

        # Act
        has_support = utils.requires_python_supports(python_requires, "2.6")

        # Assert
        self.assertEqual(has_support, "no")

    def test_no_support_but_other_2x_are(self):
        # Arrange
        python_requires = "==2.7"

        # Act
        has_support = utils.requires_python_supports(python_requires, "2.6")

        # Assert
        self.assertEqual(has_support, "no")

    def test_no_support_but_other_3x_are(self):
        # Arrange
        python_requires = ">=3.4"

        # Act
        has_support = utils.requires_python_supports(python_requires, "2.6")

        # Assert
        self.assertEqual(has_support, "no")

    def test_maybe_support_for_none(self):
        # Arrange
        # No python_requires
        python_requires = None

        # Act
        has_support = utils.requires_python_supports(python_requires, "2.6")

        # Assert
        self.assertEqual(has_support, "maybe")

    def test_maybe_support_for_empty(self):
        # Arrange
        # No python_requires
        python_requires = ""

        # Act
        has_support = utils.requires_python_supports(python_requires, "2.6")

        # Assert
        self.assertEqual(has_support, "maybe")


if __name__ == "__main__":
    unittest.main()

# End of file
