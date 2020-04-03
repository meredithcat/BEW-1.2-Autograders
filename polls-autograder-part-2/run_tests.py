import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner
from django.test.runner import DiscoverRunner
from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner

class MyRunner(DiscoverRunner):

  def run_tests(self, test_labels, extra_tests=None, **kwargs):
      """
      Run the unit tests for all the test labels in the provided list.
      Test labels should be dotted Python paths to test modules, test
      classes, or test methods.
      A list of 'extra' tests may also be provided; these tests
      will be added to the test suite.
      """
      self.setup_test_environment()
      suite = self.build_suite(test_labels, extra_tests)
      databases = self.get_databases(suite)
      old_config = self.setup_databases(aliases=databases)
      run_failed = False
      try:
          JSONTestRunner().run(suite)
      except Exception:
          run_failed = True
          raise
      finally:
          try:
              self.teardown_databases(old_config)
              self.teardown_test_environment()
          except Exception:
              # Silence teardown exceptions if an exception was raised during
              # runs to avoid shadowing it.
              if not run_failed:
                  raise

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
    django.setup()
    test_runner = MyRunner()
    test_runner.run_tests(["tests"])




# import unittest
# from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner

# if __name__ == '__main__':
#     suite = unittest.defaultTestLoader.discover('tests')
#     JSONTestRunner().run(suite)
