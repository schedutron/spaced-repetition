#!/usr/bin/env python3
"""Setup script."""
from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys

class PyTest(TestCommand):

    """Setup the py.test test runner."""

    def finalize_options(self):
        """Set options for the command line."""
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        """Execute the test runner command."""
        # Import here, because outside the required eggs aren't loaded yet
        import pytest
        sys.exit(pytest.main(self.test_args))

# Add installation instructions as well.
setup(
    name='spaced-repetition',
    tests_require=['pytest'],
    cmdclass={
        'test': PyTest
    }
)