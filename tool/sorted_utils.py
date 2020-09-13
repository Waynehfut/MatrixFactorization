# -*- coding: utf-8 -*-
"""
Created on 2018/1/24 21:39
@file: sorted_utils.py
@author: Administrator
"""

def sort_by_value(t,reverse=True):
    """
    dic中根据value排序，以[[,]]形式返回,默认降序排序，升序的话则将reverse = False
    """
    items = t.items()
    backitems = [[v[0], v[1]] for v in items]
    tt = sorted(backitems, lambda x, y: cmp(x[1], y[1]), reverse)
    return tt

def sort_by_index(t,index):
    """
    二维数组([[,,]])中根据第二维降序排序，以[[,]]形式返回
    """
    backitems = [[v[0], v[1]] for v in t]
    tt = sorted(backitems, lambda x, y: cmp(x[index], y[index]), reverse=True)
    return tt