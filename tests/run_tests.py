#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys
import os

# Add parent directory to path to ensure imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import test modules
from tests.pipeline.test_pipeline import TestTaskBase, TestDoNothing, TestManager
from tests.utils.test_path_util import TestPathUtil
from tests.utils.test_logging import TestLogging


if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    loader = unittest.TestLoader()
    test_suite.addTest(loader.loadTestsFromTestCase(TestTaskBase))
    test_suite.addTest(loader.loadTestsFromTestCase(TestDoNothing))
    test_suite.addTest(loader.loadTestsFromTestCase(TestManager))
    # test_suite.addTest(loader.loadTestsFromTestCase(TestPathUtil))
    test_suite.addTest(loader.loadTestsFromTestCase(TestLogging))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Return non-zero exit code if tests failed
    sys.exit(not result.wasSuccessful())