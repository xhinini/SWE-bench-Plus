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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 contenttypes_tests.test_operations_llm.AdditionalRenameContentTypeTests._get_schema_editor contenttypes_tests.test_operations_llm.AdditionalRenameContentTypeTests.test_clear_cache_not_called_on_integrity_error contenttypes_tests.test_operations_llm.AdditionalRenameContentTypeTests.test_save_called_with_using_db_in_rename_backward contenttypes_tests.test_operations_llm.AdditionalRenameContentTypeTests.test_save_called_with_using_db_in_rename_forward contenttypes_tests.test_operations_llm.AdditionalRenameContentTypeTests.test_update_fields_passed_correctly
coverage json -o coverage.json
: '>>>>> End Test Output'
