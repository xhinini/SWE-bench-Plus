#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_forms_llm.SaveM2MGuardRegressionTests._remove_save_m2m_and_run auth_tests.test_forms_llm.SaveM2MGuardRegressionTests.test_customuser_with_m2m_save_without_save_m2m_commit_true_does_not_raise
coverage json -o coverage.json
: '>>>>> End Test Output'
