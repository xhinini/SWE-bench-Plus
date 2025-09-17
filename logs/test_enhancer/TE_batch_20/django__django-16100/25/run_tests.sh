#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_changelist.tests_llm.test_atomic_called_on_successful_bulk_edit admin_changelist.tests_llm.test_atomic_called_when_construct_change_message_raises admin_changelist.tests_llm.test_atomic_called_when_log_change_raises_databaseerror admin_changelist.tests_llm.test_atomic_called_when_log_change_raises_on_second_form admin_changelist.tests_llm.test_atomic_called_when_no_form_has_changed admin_changelist.tests_llm.test_atomic_called_when_only_one_form_changed admin_changelist.tests_llm.test_atomic_called_when_save_form_raises admin_changelist.tests_llm.test_atomic_called_when_save_model_raises admin_changelist.tests_llm.test_atomic_called_when_save_related_raises
coverage json -o coverage.json
: '>>>>> End Test Output'
