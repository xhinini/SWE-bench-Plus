#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_storage_llm.ZeroPassPostProcessTests._run_post_process staticfiles_tests.test_storage_llm.ZeroPassPostProcessTests._write_files staticfiles_tests.test_storage_llm.make_storage_class
coverage json -o coverage.json
: '>>>>> End Test Output'
