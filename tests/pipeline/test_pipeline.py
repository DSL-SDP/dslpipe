#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import sys

from dslpipe.pipeline.pipeline import (
    TaskBase, Manager, PipelineConfigError, PipelineRuntimeError, PipelineStopIteration,
    DoNothing, OneAndOne, FileIterBase
)


class TestTaskBase(unittest.TestCase):
    """Test the TaskBase class."""

    def setUp(self):
        """Set up for tests."""
        self.params = {'tb_in': 'in_value'}
        self.task = TaskBase(self.params)

    def test_init(self):
        """Test initialization."""
        self.assertEqual(self.task.params['in'], self.params['tb_in'])

    def test_abstract_methods(self):
        """Test that abstract methods raise NotImplementedError or PipelineStopIteration."""
        self.task.setup()
        
        with self.assertRaises(PipelineStopIteration):
            self.task.next()
        
        self.task.finish()


class TestDoNothing(unittest.TestCase):
    """Test the DoNothing class."""

    def setUp(self):
        """Set up for tests."""
        self.params = {'dn_in': 'in_value'}
        self.task = DoNothing(self.params)

    def test_methods(self):
        """Test that methods don't raise exceptions."""
        self.task.setup()
        with self.assertRaises(RuntimeError):
            self.task.next('test_input')
        self.task.finish()


class TestManager(unittest.TestCase):
    """Test the Manager class."""

    def setUp(self):
        """Set up for tests."""
        self.test_pipe = {
            'pipe_copy': False,
            'pipe_tasks': [DoNothing],
            'dn_in': 'in_value'
        }
        self.manager = Manager(self.test_pipe)

    def test_init(self):
        """Test initialization."""
        self.assertEqual(len(self.manager.tasks), 1)
        self.assertEqual(self.manager.tasks[0], DoNothing)
        self.manager.run()


if __name__ == '__main__':
    unittest.main()