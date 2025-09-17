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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 contenttypes_tests.test_operations_llm.test_clear_cache_called_on_successful_rename contenttypes_tests.test_operations_llm.test_integrity_error_restores_old_model_and_does_not_clear_cache contenttypes_tests.test_operations_llm.test_missing_content_type_no_error_and_no_save_called contenttypes_tests.test_operations_llm.test_rename_does_not_affect_other_db_when_running_on_one_db contenttypes_tests.test_operations_llm.test_rename_roundtrip_forward_backward_preserves_db_alias contenttypes_tests.test_operations_llm.test_save_called_with_using_on_direct_rename_default_db contenttypes_tests.test_operations_llm.test_save_called_with_using_on_direct_rename_other_db contenttypes_tests.test_operations_llm.test_save_using_passed_in_rename_backward contenttypes_tests.test_operations_llm.test_save_using_passed_in_rename_forward
coverage json -o coverage.json
: '>>>>> End Test Output'
