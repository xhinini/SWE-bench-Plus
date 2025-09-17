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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_dateformat_llm.test_date_object_year_4_returns_04 utils_tests.test_dateformat_llm.test_year_100_returns_00 utils_tests.test_dateformat_llm.test_year_1234_returns_34 utils_tests.test_dateformat_llm.test_year_123_returns_23 utils_tests.test_dateformat_llm.test_year_1900_returns_00 utils_tests.test_dateformat_llm.test_year_1_returns_01 utils_tests.test_dateformat_llm.test_year_2000_returns_00 utils_tests.test_dateformat_llm.test_year_2005_returns_05 utils_tests.test_dateformat_llm.test_year_999_returns_99 utils_tests.test_dateformat_llm.test_year_99_returns_99
coverage json -o coverage.json
: '>>>>> End Test Output'
