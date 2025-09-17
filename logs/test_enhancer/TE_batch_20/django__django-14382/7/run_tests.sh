#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.test_trailing_dot_variant_1 admin_scripts.tests_llm.test_trailing_dot_variant_10 admin_scripts.tests_llm.test_trailing_dot_variant_2 admin_scripts.tests_llm.test_trailing_dot_variant_3 admin_scripts.tests_llm.test_trailing_dot_variant_4 admin_scripts.tests_llm.test_trailing_dot_variant_5 admin_scripts.tests_llm.test_trailing_dot_variant_6 admin_scripts.tests_llm.test_trailing_dot_variant_7 admin_scripts.tests_llm.test_trailing_dot_variant_8 admin_scripts.tests_llm.test_trailing_dot_variant_9
coverage json -o coverage.json
: '>>>>> End Test Output'
