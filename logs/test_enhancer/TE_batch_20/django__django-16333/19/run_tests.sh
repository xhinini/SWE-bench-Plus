#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_forms_llm.SaveM2MGuardTests._make_and_save_user auth_tests.test_forms_llm.SaveM2MGuardTests._restore_save_m2m auth_tests.test_forms_llm.SaveM2MGuardTests._temporarily_remove_save_m2m
coverage json -o coverage.json
: '>>>>> End Test Output'
