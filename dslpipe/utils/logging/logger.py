#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
日志系统模块，提供完整的日志记录、查询和分析功能。
支持不同级别的日志输出，包括DEBUG、INFO、WARNING、ERROR、CRITICAL。
"""

import os
import sys
import logging
import datetime
import json
import re
from enum import Enum
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler


class LogLevel(Enum):
    """日志级别枚举类"""
    NOTSET = logging.NOTSET
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class DSLPipeLogger:
    """DSLPipe日志记录器类"""
    
    def __init__(self, name, level=LogLevel.INFO, log_file=None, max_bytes=10*1024*1024, 
                 backup_count=5, format_str=None, console_output=True):
        """
        初始化日志记录器
        
        参数:
            name (str): 日志记录器名称
            level (LogLevel): 日志级别
            log_file (str): 日志文件路径，如果为None则不记录到文件
            max_bytes (int): 单个日志文件最大字节数
            backup_count (int): 备份日志文件数量
            format_str (str): 日志格式字符串
            console_output (bool): 是否输出到控制台
        """
        self.name = name
        self.level = level.value if isinstance(level, LogLevel) else level
        self.log_file = log_file
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.format_str = format_str or '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        self.console_output = console_output
        
        # 创建日志记录器
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.level)
        
        # 清除已有的处理器
        # if self.logger.handlers:
        #     self.logger.handlers.clear()
        
        # 检查是否已经有处理器，避免重复添加
        if not self.logger.handlers:
            # 创建格式化器
            formatter = logging.Formatter(self.format_str)
            
            # 添加控制台处理器
            if console_output:
                console_handler = logging.StreamHandler(sys.stdout)
                console_handler.setFormatter(formatter)
                self.logger.addHandler(console_handler)
            
            # 添加文件处理器
            if log_file:
                # 确保日志目录存在
                log_dir = os.path.dirname(log_file)
                if log_dir and not os.path.exists(log_dir):
                    os.makedirs(log_dir)
                    
                # 创建文件处理器
                file_handler = RotatingFileHandler(
                    log_file, maxBytes=max_bytes, backupCount=backup_count
                )
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
        
        # 阻止日志消息传播到根日志记录器，避免重复输出
        self.logger.propagate = False
    
    def debug(self, message, *args, **kwargs):
        """记录DEBUG级别日志"""
        self.logger.debug(message, *args, **kwargs)
    
    def info(self, message, *args, **kwargs):
        """记录INFO级别日志"""
        self.logger.info(message, *args, **kwargs)
    
    def warning(self, message, *args, **kwargs):
        """记录WARNING级别日志"""
        self.logger.warning(message, *args, **kwargs)
    
    def error(self, message, *args, **kwargs):
        """记录ERROR级别日志"""
        self.logger.error(message, *args, **kwargs)
    
    def critical(self, message, *args, **kwargs):
        """记录CRITICAL级别日志"""
        self.logger.critical(message, *args, **kwargs)
    
    def exception(self, message, *args, exc_info=True, **kwargs):
        """记录异常信息"""
        self.logger.exception(message, *args, exc_info=exc_info, **kwargs)


class LogAnalyzer:
    """日志分析器类，用于查询和分析日志"""
    
    def __init__(self, log_file):
        """
        初始化日志分析器
        
        参数:
            log_file (str): 日志文件路径
        """
        self.log_file = log_file
        self._validate_log_file()
    
    def _validate_log_file(self):
        """验证日志文件是否存在"""
        if not os.path.exists(self.log_file):
            raise FileNotFoundError(f"日志文件不存在: {self.log_file}")
    
    def query_by_level(self, level):
        """
        按日志级别查询日志
        
        参数:
            level (LogLevel): 日志级别
        
        返回:
            list: 符合条件的日志记录列表
        """
        level_str = level.name if isinstance(level, LogLevel) else level
        return self.query_by_pattern(f" - {level_str} - ")
    
    def query_by_time_range(self, start_time, end_time):
        """
        按时间范围查询日志
        
        参数:
            start_time (datetime): 开始时间
            end_time (datetime): 结束时间
        
        返回:
            list: 符合条件的日志记录列表
        """
        results = []
        time_pattern = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})')
        
        with open(self.log_file, 'r') as f:
            for line in f:
                match = time_pattern.search(line)
                if match:
                    log_time_str = match.group(1)
                    try:
                        log_time = datetime.datetime.strptime(
                            log_time_str, '%Y-%m-%d %H:%M:%S,%f'
                        )
                        if start_time <= log_time <= end_time:
                            results.append(line.strip())
                    except ValueError:
                        continue
        
        return results
    
    def query_by_pattern(self, pattern):
        """
        按模式查询日志
        
        参数:
            pattern (str): 查询模式（正则表达式）
        
        返回:
            list: 符合条件的日志记录列表
        """
        results = []
        
        with open(self.log_file, 'r') as f:
            for line in f:
                if re.search(pattern, line):
                    results.append(line.strip())
        
        return results
    
    def get_level_statistics(self):
        """
        获取各日志级别的统计信息
        
        返回:
            dict: 各日志级别的统计信息
        """
        stats = {level.name: 0 for level in LogLevel}
        
        for level in LogLevel:
            stats[level.name] = len(self.query_by_level(level))
        
        return stats
    
    def export_to_json(self, output_file, logs):
        """
        将日志导出为JSON格式
        
        参数:
            output_file (str): 输出文件路径
            logs (list): 日志记录列表
        """
        with open(output_file, 'w') as f:
            json.dump(logs, f, indent=2)


# 全局日志记录器字典
_loggers = {}

# 全局默认日志级别：未显式指定 level 时，新创建的 logger 都使用此级别。
# 可由 Manager.set_default_level 在解析 pipefile 后更新。
_default_level = LogLevel.INFO


def get_logger(name, level=None, log_file=None, max_bytes=10*1024*1024,
               backup_count=5, format_str=None, console_output=True):
    """
    获取日志记录器

    参数:
        name (str): 日志记录器名称
        level (LogLevel or int or None): 日志级别。为 None 时使用全局默认级别
            (可通过 :func:`set_default_level` 设置)。
        log_file (str): 日志文件路径，如果为None则不记录到文件
        max_bytes (int): 单个日志文件最大字节数
        backup_count (int): 备份日志数量
        format_str (str): 日志格式字符串
        console_output (bool): 是否输出到控制台

    返回:
        DSLPipeLogger: 日志记录器实例
    """
    global _loggers

    if name not in _loggers:
        effective_level = level if level is not None else _default_level
        _loggers[name] = DSLPipeLogger(
            name, effective_level, log_file, max_bytes, backup_count, format_str, console_output
        )
    elif level is not None:
        # 调用方显式给了 level：尊重显式设置，更新已存在 logger 的级别
        resolved = level.value if isinstance(level, LogLevel) else level
        _loggers[name].level = resolved
        _loggers[name].logger.setLevel(resolved)

    return _loggers[name]


def set_default_level(level):
    """设置全局默认日志级别，并同步更新所有已存在的 logger。

    应在解析 pipefile 中的 ``logging`` 参数后立即调用，以便把级别下发到
    所有已通过 ``import`` 创建的 task logger，以及后续通过 ``get_logger``
    动态创建的新 logger。

    参数:
        level (LogLevel or int or str): 新的默认级别。可以是
            :class:`LogLevel` 枚举、整数值，或字符串（如 ``"DEBUG"``）。

    抛出:
        TypeError: 当 ``level`` 不是 ``LogLevel``/``int``/``str`` 时。
        ValueError: 当字符串或整数无法映射到已知的日志级别时（错误信息
            会列出所有合法级别名称，便于排查 pipefile 拼写错误）。
    """
    global _default_level

    valid_names = [m.name for m in LogLevel]

    if isinstance(level, LogLevel):
        resolved = level
    elif isinstance(level, str):
        try:
            resolved = LogLevel[level.upper()]
        except KeyError:
            raise ValueError(
                f"无效的日志级别字符串: {level!r}。"
                f"合法值: {', '.join(valid_names)}。"
            ) from None
    elif isinstance(level, int) and not isinstance(level, bool):
        try:
            resolved = LogLevel(level)
        except ValueError:
            raise ValueError(
                f"无效的日志级别整数值: {level}。"
                f"合法值: {', '.join(f'{m.name}={m.value}' for m in LogLevel)}。"
            ) from None
    else:
        raise TypeError(
            f"level 参数必须是 LogLevel 枚举、int 或 str，"
            f"实际收到 {type(level).__name__}: {level!r}。"
        )

    _default_level = resolved

    # 同步更新所有已存在 logger（这些通常是 task 模块 import 时创建的）
    for lg in _loggers.values():
        lg.level = resolved.value
        lg.logger.setLevel(resolved.value)


def setup_logging(default_level=LogLevel.INFO, log_dir=None, log_filename=None):
    """设置全局日志配置。

    该函数做两件事：
      1. 通过 :func:`set_default_level` 把默认日志级别下发到所有已存在的
         logger 和后续新创建的 logger（真正"全局"）。
      2. 在 ``log_dir`` 下创建根 ``dslpipe`` logger（带轮转文件处理器）。

    调用方只需要关心 ``default_level``，不需要再单独调用
    :func:`set_default_level`，避免级别被双写。

    参数:
        default_level (LogLevel or int or str): 默认日志级别。
        log_dir (str): 日志目录，如果为 None 则使用当前目录下的 logs 目录。
        log_filename (str): 日志文件名，如果为 None 则使用 dslpipe.log。

    返回:
        DSLPipeLogger: 根 dslpipe 日志记录器实例。
    """
    # 先全局下发默认级别，确保所有 import 时就创建好的 task logger 也跟着
    # 切到新级别。传 None 给 get_logger 让它走 _default_level 单一来源，
    # 避免在这里和 set_default_level 内部对同一 logger 二次 setLevel。
    set_default_level(default_level)

    if log_dir is None:
        log_dir = os.path.join(os.getcwd(), 'logs')

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    if log_filename is None:
        log_filename = 'dslpipe.log'

    log_file = os.path.join(log_dir, log_filename)

    return get_logger('dslpipe', level=None, log_file=log_file)