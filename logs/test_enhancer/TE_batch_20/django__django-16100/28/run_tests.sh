#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_changelist.tests_llm._post_changelist_and_capture_atomic_kwargs admin_changelist.tests_llm.test_atomic_called_with_using_for_multiple_changed_forms admin_changelist.tests_llm.test_atomic_called_with_using_on_successful_list_editable_save admin_changelist.tests_llm.test_atomic_called_with_using_when_all_forms_unchanged_but_valid admin_changelist.tests_llm.test_atomic_called_with_using_when_construct_change_message_raises admin_changelist.tests_llm.test_atomic_called_with_using_when_log_change_raises admin_changelist.tests_llm.test_atomic_called_with_using_when_save_model_fails_on_second_form admin_changelist.tests_llm.test_atomic_called_with_using_when_save_model_raises admin_changelist.tests_llm.test_atomic_called_with_using_when_save_related_raises
coverage json -o coverage.json
: '>>>>> End Test Output'
