#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import tempfile

from dslpipe.utils.path_util import iter_path, input_path, output_path


class TestPathUtil(unittest.TestCase):
    """Test the path_util module."""

    def setUp(self):
        """Set up for tests."""
        self.test_path = '/test/path/file.txt'
        # Save original TL_OUTPUT environment variable
        self.original_tl_output = os.environ.get('TL_OUTPUT')
        # Set test TL_OUTPUT
        self.temp_dir = tempfile.mkdtemp()
        os.environ['TL_OUTPUT'] = self.temp_dir

    def tearDown(self):
        """Clean up after tests."""
        # Restore original TL_OUTPUT
        if self.original_tl_output:
            os.environ['TL_OUTPUT'] = self.original_tl_output
        else:
            del os.environ['TL_OUTPUT']
        # Remove temp directory
        os.rmdir(self.temp_dir)

    def test_iter_path(self):
        """Test iter_path function."""
        # Test with iteration number
        result = iter_path(self.test_path, 5)
        self.assertEqual(result, '/test/path/file_5.txt')
        
        # Test with no iteration number
        result = iter_path(self.test_path)
        self.assertEqual(result, self.test_path)

    def test_input_path(self):
        """Test input_path function."""
        # Test with absolute path
        result = input_path(self.test_path)
        self.assertEqual(result, self.test_path)
        
        # Test with relative path
        rel_path = 'relative/path/file.txt'
        expected = os.path.join(self.temp_dir, rel_path)
        result = input_path(rel_path)
        self.assertEqual(result, expected)

    def test_output_path(self):
        """Test output_path function."""
        # Test with absolute path
        result = output_path(self.test_path)
        self.assertEqual(result, self.test_path)
        
        # Test with relative path
        rel_path = 'relative/path/file.txt'
        expected = os.path.join(self.temp_dir, rel_path)
        result = output_path(rel_path)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()