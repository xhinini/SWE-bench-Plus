#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_dateformat_llm.test_Y_concatenation_works utils_tests.test_dateformat_llm.test_Y_format_year_0001_datetime utils_tests.test_dateformat_llm.test_Y_format_year_0004_datetime utils_tests.test_dateformat_llm.test_Y_format_year_0042_date utils_tests.test_dateformat_llm.test_Y_format_year_0123_datetime utils_tests.test_dateformat_llm.test_Y_format_year_0999_datetime utils_tests.test_dateformat_llm.test_Y_format_year_1000_boundary utils_tests.test_dateformat_llm.test_Y_format_year_9999_upper_bound utils_tests.test_dateformat_llm.test_Y_return_type_is_string utils_tests.test_dateformat_llm.test_composite_format_Y_and_y
coverage json -o coverage.json
: '>>>>> End Test Output'
