#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.ManageRunserverAddrFormattingTests.test_run_called_with_zero_expands_to_0_0_0_0 admin_scripts.tests_llm.ManageRunserverAddrFormattingTests.test_zero_addr_with_checks_enabled_still_reports_expanded_address
coverage json -o coverage.json
: '>>>>> End Test Output'
