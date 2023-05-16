# -*- coding: utf-8 -*-

"""
@file    : decorator
@author  : wieszheng
@Data    : 2023/5/17 0:18
@software: PyCharm
"""
import types


class DataDrive:
    """数据驱动类修饰器，标识一个测试用例类使用数据驱动"""

    def __init__(self, case_data):
        """构造函数

        :param case_datas: 数据驱动测试数据集
        :type case_datas: list/tuple/dict
        """
        self._case_data = case_data

    def __call__(self, testcase_class):
        """修饰器

        :param testcase_class: 要修饰的测试用例
        :type testcase_class: TestCase
        """
        # if not issubclass(testcase_class, TestCase):
        #     raise TypeError(
        #         "The data driver decorator cannot be applied to non TestCase classes"
        #     )
        testcase_class.__qtaf_datadrive__ = self
        return testcase_class

    def __iter__(self):
        """遍历全部的数据名"""
        if isinstance(self._case_data, types.GeneratorType):
            self._case_data = list(self._case_data)
        if isinstance(self._case_data, list) or isinstance(self._case_data, tuple):
            for it in range(len(self._case_data)):
                yield it
        else:
            for it in self._case_data:
                yield it

    def __getitem__(self, name):
        """获取对应名称的数据"""
        return self._case_data[name]

    def __len__(self):
        return len(self._case_data)
