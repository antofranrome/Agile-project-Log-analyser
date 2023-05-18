import unittest
from parse import compile
from parse import with_pattern
import datetime as dt
import pandas as pd
import json
import unittest

def create_log_list(log_file):
    logs = open(log_file)
    lines = logs.readlines()
    log_list = []
    log = ''
    for line in lines:
        if line[:11] == "2014/Oct/24":
            log_list.append(log)
            log = line
        else:
            log += line

    log_list = log_list[1:]
    return log_list

class TestCreateLogList(unittest.TestCase):
    def test_empty_log_file(self):
        # Test case 1: Empty log file
        log_file = 'empty_log.txt'
        expected_output = []
        self.assertEqual(create_log_list(log_file), expected_output)

    def test_no_matching_logs(self):
        # Test case 2: Log file without any matching logs
        log_file = 'no_matching_logs.txt'
        expected_output = []
        self.assertEqual(create_log_list(log_file), expected_output)

    def test_matching_logs(self):
        # Test case 3: Log file with matching logs
        log_file = 'matching_logs.txt'
        expected_output = [
            "2014/Oct/24 Log line 1\n",
            "2014/Oct/24 Log line 2\n",
            "2014/Oct/24 Log line 3\n"
        ]
        self.assertEqual(create_log_list(log_file), expected_output)

if __name__ == '__main__':
    unittest.main()

