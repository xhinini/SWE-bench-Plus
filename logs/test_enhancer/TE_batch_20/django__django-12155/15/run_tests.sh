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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_docs.test_utils_llm.ParseDocstringCleandocTests.assert_matches_cleandoc admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_complex_mixed_indentation_example admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_with_leading_blank_line_and_extra_indent
coverage json -o coverage.json
: '>>>>> End Test Output'
