#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_changelist.tests_llm.test_changelist_atomic_called_even_if_no_forms_changed admin_changelist.tests_llm.test_changelist_atomic_called_when_action_selected_but_saving_list_editable admin_changelist.tests_llm.test_changelist_atomic_called_when_log_change_raises_on_second admin_changelist.tests_llm.test_changelist_atomic_called_with_extra_post_params admin_changelist.tests_llm.test_changelist_atomic_called_with_ordering_param admin_changelist.tests_llm.test_changelist_atomic_called_with_single_form admin_changelist.tests_llm.test_changelist_atomic_called_with_three_forms admin_changelist.tests_llm.test_changelist_atomic_used_when_log_change_raises admin_changelist.tests_llm.test_changelist_atomic_uses_router_db_for_simple_save
coverage json -o coverage.json
: '>>>>> End Test Output'
