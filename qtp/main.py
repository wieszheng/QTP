# -*- coding: utf-8 -*-

"""
@file    : main.py
@author  : v_wieszheng
@Data    : 2023/5/17 0:15
@software: PyCharm
"""
import inspect
import sys
import traceback


class TestResult:
    def __init__(self, test_case_name):
        self.test_case_name = test_case_name
        self.passed = 0
        self.failed = 0
        self.errors = []

    def add_pass(self):
        self.passed += 1

    def add_fail(self):
        self.failed += 1

    def add_error(self, exception):
        self.errors.append(exception)


class sTestCase:
    def __init__(self, name):
        self.name = name

    def assertEqual(self, actual, expected):
        assert actual == expected, f"{actual} != {expected}"

    def assertTrue(self, condition):
        assert condition, "Condition is not true"

    def assertFalse(self, condition):
        assert not condition, "Condition is not false"

    # 其他更多断言方法

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def run(self):
        result = TestResult(self.name)
        try:
            self.setUp()
            getattr(self, self.name)()
            self.tearDown()
            result.add_pass()
        except AssertionError as e:
            result.add_fail()
            result.add_error(e)
        except Exception as e:
            result.add_error(traceback.format_exception(type(e), e, e.__traceback__))

        return result


class TestSuite:
    def __init__(self):
        self.test_cases = []

    def add_test_case(self, test_case):
        self.test_cases.append(test_case)

    def run(self):
        passed = 0
        failed = 0
        errors = []
        for test_case in self.test_cases:
            result = test_case.run()
            passed += result.passed
            failed += result.failed
            errors += result.errors

        print(f"{len(self.test_cases)} test cases, {passed} passed, {failed} failed")
        if len(errors) > 0:
            print("Errors:")
            for error in errors:
                print(error)


def discover_tests(module_name):
    module = __import__(module_name)
    test_suites = []

    for attribute_name in dir(module):
        class_or_function = getattr(module, attribute_name)
        if inspect.isclass(class_or_function):     # 检查是否为类
            class_name = class_or_function.__name__
            if class_name.startswith("Test"):     # 找到以 "Test" 开头的类
                suite = build_test_suite(class_or_function)
                test_suites.append(suite)

    return TestSuiteBuilder.merge(*test_suites)


class TestSuiteBuilder:
    @staticmethod
    def merge(*test_suites):
        merged_suite = TestSuite()
        for suite in test_suites:
            for test_case in suite.test_cases:
                merged_suite.add_test_case(test_case)
        return merged_suite


def build_test_suite(test_case_class):
    suite = TestSuite()
    for name in dir(test_case_class):
        if name.startswith('test'):
            suite.add_test_case(test_case_class(name))
    return suite

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) > 0:
        module_name = args[0].replace('.py', '')
        suite = discover_tests(module_name)
        suite.run()
    else:
        print("Usage: python test_runner.py [test_module]")




