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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_loader_llm.MigrationLoaderPathTests._run_with_module_state migrations.test_loader_llm.MigrationLoaderPathTests.test_module_file_with_file_present_no_path migrations.test_loader_llm.MigrationLoaderPathTests.test_module_file_without_path_and_no_file migrations.test_loader_llm.MigrationLoaderPathTests.test_namespace_package_no_file_with_custom_path_object migrations.test_loader_llm.MigrationLoaderPathTests.test_namespace_package_no_file_with_tuple_path migrations.test_loader_llm.MigrationLoaderPathTests.test_package_no_file_with_path_being_iterator_object migrations.test_loader_llm.MigrationLoaderPathTests.test_package_with_file_and_custom_path_object migrations.test_loader_llm.MigrationLoaderPathTests.test_package_with_file_and_tuple_path migrations.test_loader_llm.MigrationLoaderPathTests.test_regular_package_no_file_with_list_path migrations.test_loader_llm.MigrationLoaderPathTests.test_regular_package_no_file_with_list_subclass_path migrations.test_loader_llm.MigrationLoaderPathTests.test_restore_module_state_after_load_disk
coverage json -o coverage.json
: '>>>>> End Test Output'
