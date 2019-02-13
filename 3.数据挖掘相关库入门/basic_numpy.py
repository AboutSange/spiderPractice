#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Numpy 提供数组支持，以及相应的高效的处理函数
"""

import numpy as np  # 一般以np作为numpy的别名

a = np.array([2, 0, 1, 5])  # 一维数组
print(a)  # [2 0 1 5]
print(type(a))  # <type 'numpy.ndarray'>
print(a[:3])
print(a.min())
a.sort()
print(a)  # [0 1 2 5]

b = np.array([[1, 2, 3], [4, 5, 6]])  # 二维数组
print(b)
