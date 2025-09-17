#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
export LANG=en_US.UTF-8
export LANGUAGE=en_US:en
export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf8
python --version && python -m pip install -U pip
python -m pip install -U 'coverage==6.2'

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 contenttypes_tests.test_operations_llm.test__rename_backward_respects_db_alias contenttypes_tests.test_operations_llm.test__rename_conflict_on_other_db_does_not_affect_default contenttypes_tests.test_operations_llm.test__rename_conflict_on_other_db_resets_model contenttypes_tests.test_operations_llm.test__rename_does_not_update_default_db contenttypes_tests.test_operations_llm.test__rename_missing_content_type_is_noop contenttypes_tests.test_operations_llm.test__rename_skips_when_router_disallows_migration contenttypes_tests.test_operations_llm.test__rename_succeeds_when_default_db_has_conflict contenttypes_tests.test_operations_llm.test__rename_transaction_atomic_uses_correct_db contenttypes_tests.test_operations_llm.test__rename_uses_schema_editor_db_alias
coverage json -o coverage.json
: '>>>>> End Test Output'
