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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_loader_llm._get_migrations_for_module_state migrations.test_loader_llm.test_custom_path_obj_treated_as_namespace migrations.test_loader_llm.test_file_present_but_path_tuple_loads_migrations migrations.test_loader_llm.test_list_path_with_no_file_is_accepted migrations.test_loader_llm.test_list_subclass_path_treated_as_regular_package migrations.test_loader_llm.test_namespace_with_has_location_false_and_no_file migrations.test_loader_llm.test_non_string_elements_in_list_path_still_treated_as_list_package migrations.test_loader_llm.test_original_path_restored_after_changes migrations.test_loader_llm.test_removing_path_attribute_results_in_unmigrated migrations.test_loader_llm.test_tuple_path_treated_as_namespace
coverage json -o coverage.json
: '>>>>> End Test Output'
