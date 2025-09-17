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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_loader_llm.AdditionalLoaderTests._make_migration_submodule migrations.test_loader_llm.AdditionalLoaderTests._make_package_module migrations.test_loader_llm.AdditionalLoaderTests.test_loading_actual_migration_submodule_when_package_has_no_file_but_list_path migrations.test_loader_llm.AdditionalLoaderTests.test_non_list_path_with_file_present_is_migrated migrations.test_loader_llm.AdditionalLoaderTests.test_regular_package_no_file_and_list_subclass_is_migrated migrations.test_loader_llm.AdditionalLoaderTests.test_regular_package_no_file_path_list_is_migrated
coverage json -o coverage.json
: '>>>>> End Test Output'
