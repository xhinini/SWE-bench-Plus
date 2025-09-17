#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_changelist.tests_llm.test_atomic_not_used_when_formset_invalid admin_changelist.tests_llm.test_atomic_respects_router_db_for_write_override admin_changelist.tests_llm.test_atomic_used_even_if_no_forms_changed admin_changelist.tests_llm.test_atomic_used_on_list_editable_success admin_changelist.tests_llm.test_atomic_used_when_log_change_raises admin_changelist.tests_llm.test_atomic_used_when_multiple_forms_changed admin_changelist.tests_llm.test_atomic_used_when_save_form_raises admin_changelist.tests_llm.test_atomic_used_when_save_model_raises admin_changelist.tests_llm.test_atomic_used_when_save_related_raises
coverage json -o coverage.json
: '>>>>> End Test Output'
