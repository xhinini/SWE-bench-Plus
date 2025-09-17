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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_docstring_only_whitespace admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_docstring_with_leading_blank_line admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_docstring_with_no_body_but_metadata admin_docs.test_utils_llm._expected_parse_docstring
coverage json -o coverage.json
: '>>>>> End Test Output'
