#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
export LANG=en_US.UTF-8
export LANGUAGE=en_US:en
export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf8
python --version && python -m pip install -U pip
python -m pip install -U 'coverage==6.2'

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_dateformat_llm.test_y_combined_with_Y utils_tests.test_dateformat_llm.test_y_date_object_returns_two_digits utils_tests.test_dateformat_llm.test_y_max_year_9999 utils_tests.test_dateformat_llm.test_y_single_digit_year utils_tests.test_dateformat_llm.test_y_two_digit_year_99 utils_tests.test_dateformat_llm.test_y_using_dateformat_class_directly utils_tests.test_dateformat_llm.test_y_year_100_returns_00 utils_tests.test_dateformat_llm.test_y_year_123_returns_23 utils_tests.test_dateformat_llm.test_y_year_1999_returns_99 utils_tests.test_dateformat_llm.test_y_year_2000_returns_00
coverage json -o coverage.json
: '>>>>> End Test Output'
