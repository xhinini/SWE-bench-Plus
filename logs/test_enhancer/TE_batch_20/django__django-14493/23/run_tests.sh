#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_storage_llm.TestStorage.__init__ staticfiles_tests.test_storage_llm.ZeroPassesPostProcessTests._write_file staticfiles_tests.test_storage_llm.ZeroPassesPostProcessTests.setUp staticfiles_tests.test_storage_llm.ZeroPassesPostProcessTests.test_post_process_respects_dry_run
coverage json -o coverage.json
: '>>>>> End Test Output'
