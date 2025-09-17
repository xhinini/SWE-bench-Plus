#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_changelist.tests_llm.test_atomic_called_even_if_no_forms_have_changed admin_changelist.tests_llm.test_atomic_called_once_for_multiple_changed_forms admin_changelist.tests_llm.test_atomic_called_with_using_on_list_editable_success admin_changelist.tests_llm.test_atomic_called_with_using_on_list_editable_when_log_change_raises admin_changelist.tests_llm.test_atomic_called_with_using_on_list_editable_when_save_model_raises admin_changelist.tests_llm.test_atomic_context_manager_enter_exit_called admin_changelist.tests_llm.test_atomic_not_called_if_formset_invalid admin_changelist.tests_llm.test_atomic_not_called_if_no_list_editable_configured admin_changelist.tests_llm.test_atomic_uses_router_db_for_write_non_default_alias
coverage json -o coverage.json
: '>>>>> End Test Output'
