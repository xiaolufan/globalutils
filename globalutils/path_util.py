#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Mr Fan
# @Time: 2021年06月25
"""
Introduction:

"""
import sys
import os
from globalutils.logger import logger


def joinPath(left_path:str, right_path:str)->str:
    """
    将做路径与右路径进行连接
    :param left_path: 左路径
    :param right_path: 右路径
    :return: 拼接后的路径
    """
    return os.path.join(left_path,right_path)


if __name__ == "__main__":
    pass