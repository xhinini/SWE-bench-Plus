#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_forms_llm.SaveM2MRegressionTests._remove_save_m2m auth_tests.test_forms_llm.SaveM2MRegressionTests._restore_save_m2m auth_tests.test_forms_llm.SaveM2MRegressionTests._unique_username
coverage json -o coverage.json
: '>>>>> End Test Output'
