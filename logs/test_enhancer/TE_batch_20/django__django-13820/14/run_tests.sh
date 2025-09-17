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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_loader_llm.LoaderModuleAttributesTests._run_loader_with_module migrations.test_loader_llm.LoaderModuleAttributesTests.setUp migrations.test_loader_llm.LoaderModuleAttributesTests.test_custom_path_object_that_is_list_subclass_loads migrations.test_loader_llm.LoaderModuleAttributesTests.test_empty_list_path_with_no_file_counts_as_migrated migrations.test_loader_llm.LoaderModuleAttributesTests.test_list_subclass_path_with_no_file_loads migrations.test_loader_llm.LoaderModuleAttributesTests.test_module_file_without_path_ignored migrations.test_loader_llm.LoaderModuleAttributesTests.test_namespace_package_ignored_based_on_path_type migrations.test_loader_llm.LoaderModuleAttributesTests.test_no_file_no_path_attribute_ignored migrations.test_loader_llm.LoaderModuleAttributesTests.test_package_with_non_none_file_and_path_list_loads migrations.test_loader_llm.LoaderModuleAttributesTests.test_regular_package_without_file_loads_migrations migrations.test_loader_llm.LoaderModuleAttributesTests.test_tuple_path_and_no_file_ignored
coverage json -o coverage.json
: '>>>>> End Test Output'
