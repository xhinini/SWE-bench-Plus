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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_dateformat_llm.test_y_year_1 utils_tests.test_dateformat_llm.test_y_year_10 utils_tests.test_dateformat_llm.test_y_year_100 utils_tests.test_dateformat_llm.test_y_year_1000 utils_tests.test_dateformat_llm.test_y_year_101 utils_tests.test_dateformat_llm.test_y_year_123 utils_tests.test_dateformat_llm.test_y_year_200 utils_tests.test_dateformat_llm.test_y_year_2003 utils_tests.test_dateformat_llm.test_y_year_99 utils_tests.test_dateformat_llm.test_y_year_999
coverage json -o coverage.json
: '>>>>> End Test Output'
