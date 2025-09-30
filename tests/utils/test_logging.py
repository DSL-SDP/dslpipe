#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import tempfile
import shutil
import datetime
import logging
from dslpipe.utils.logging import get_logger, LogLevel, LogAnalyzer, setup_logging


class TestLogging(unittest.TestCase):
    """测试日志系统模块"""

    def setUp(self):
        """测试前准备"""
        self.test_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.test_dir, 'test.log')
        self.logger_name = self._testMethodName

    def tearDown(self):
        """测试后清理"""
        # 关闭并移除所有日志处理器
        logger = logging.getLogger(self.logger_name)
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)
        
        # 清除全局日志记录器缓存
        from dslpipe.utils.logging.logger import _loggers
        if self.logger_name in _loggers:
            del _loggers[self.logger_name]
        
        # 删除测试目录
        shutil.rmtree(self.test_dir)

    def test_logger_levels(self):
        """测试不同级别的日志输出"""
        # 确保日志目录存在
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        # 获取日志记录器
        logger = get_logger(self.logger_name, level=LogLevel.DEBUG, log_file=self.log_file, console_output=False)
        
        # 记录不同级别的日志
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")
        
        # 确保日志被写入文件
        for handler in logger.logger.handlers:
            handler.flush()
        
        # 验证日志文件内容
        with open(self.log_file, 'r') as f:
            content = f.read()
            
        self.assertIn("Debug message", content)
        self.assertIn("Info message", content)
        self.assertIn("Warning message", content)
        self.assertIn("Error message", content)
        self.assertIn("Critical message", content)

    def test_log_analyzer(self):
        """测试日志分析功能"""
        # 确保日志目录存在
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        # 获取日志记录器
        logger = get_logger(self.logger_name, level=LogLevel.DEBUG, log_file=self.log_file, console_output=False)
        
        # 记录不同级别的日志
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")
        
        # 确保日志被写入文件
        for handler in logger.logger.handlers:
            handler.flush()
        
        analyzer = LogAnalyzer(self.log_file)
        
        # 测试按级别查询
        debug_logs = analyzer.query_by_level(LogLevel.DEBUG)
        self.assertEqual(len(debug_logs), 1)
        self.assertIn("Debug message", debug_logs[0])
        
        # 测试按模式查询
        warning_logs = analyzer.query_by_pattern("Warning")
        self.assertEqual(len(warning_logs), 1)
        self.assertIn("Warning message", warning_logs[0])
        
        # 测试统计功能
        stats = analyzer.get_level_statistics()
        self.assertEqual(stats["DEBUG"], 1)
        self.assertEqual(stats["INFO"], 1)
        self.assertEqual(stats["WARNING"], 1)
        self.assertEqual(stats["ERROR"], 1)
        self.assertEqual(stats["CRITICAL"], 1)


if __name__ == '__main__':
    unittest.main()