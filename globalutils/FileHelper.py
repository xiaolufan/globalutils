#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Mr Fan
# @Time: 2021年06月25
"""
Introduction:

"""
import os
from globalutils.logger import logger
from globalutils.data_util import read_json
from globalutils.path_util import joinPath


PROJECT_ROOT_PATH = os.getenv("PROJECT_ROOT_PATH")
if PROJECT_ROOT_PATH is None:
    logger.error("PROJECT_ROOT_PATH IS NOT PASSED!")
    raise ValueError

# 配置文件内容
FILE_ROOT_INFO = read_json(joinPath(PROJECT_ROOT_PATH, "config.json"))
# 数据库文件内容
DB_ROOT_INFO = read_json(joinPath(PROJECT_ROOT_PATH, "db.json"))




if __name__ == "__main__":
    pass