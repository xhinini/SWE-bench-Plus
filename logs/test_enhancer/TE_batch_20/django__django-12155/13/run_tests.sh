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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_docs.test_utils_llm.ParseDocstringCleandocTests.assert_body_leading_spaces admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_case_1 admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_case_10 admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_case_2 admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_case_3 admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_case_4 admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_case_5 admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_case_6 admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_case_7 admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_case_8 admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_case_9 admin_docs.test_utils_llm.make_doc
coverage json -o coverage.json
: '>>>>> End Test Output'
