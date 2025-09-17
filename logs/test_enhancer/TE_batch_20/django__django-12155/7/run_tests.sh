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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_docs.test_utils_llm.ParseDocstringRegressionTests.test_parse_docstring_first_line_unindented_rest_indented admin_docs.test_utils_llm.ParseDocstringRegressionTests.test_parse_docstring_leading_blank_line_and_indentation admin_docs.test_utils_llm.ParseDocstringRegressionTests.test_parse_docstring_matches_cleandoc_behavior admin_docs.test_utils_llm.ParseDocstringRegressionTests.test_parse_rst_with_docstring_indentation_removed
coverage json -o coverage.json
: '>>>>> End Test Output'
