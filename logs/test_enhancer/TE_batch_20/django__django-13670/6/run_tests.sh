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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_dateformat_llm.test_year_format_1 utils_tests.test_dateformat_llm.test_year_format_100 utils_tests.test_dateformat_llm.test_year_format_101 utils_tests.test_dateformat_llm.test_year_format_12 utils_tests.test_dateformat_llm.test_year_format_123 utils_tests.test_dateformat_llm.test_year_format_200 utils_tests.test_dateformat_llm.test_year_format_9 utils_tests.test_dateformat_llm.test_year_format_909 utils_tests.test_dateformat_llm.test_year_format_99 utils_tests.test_dateformat_llm.test_year_format_999
coverage json -o coverage.json
: '>>>>> End Test Output'
