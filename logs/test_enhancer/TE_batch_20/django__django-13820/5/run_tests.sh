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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_loader_llm.MigrationModuleClassificationTests.insert_module migrations.test_loader_llm.MigrationModuleClassificationTests.make_app_config migrations.test_loader_llm.MigrationModuleClassificationTests.test_existing_module_is_reloaded_and_classified migrations.test_loader_llm.MigrationModuleClassificationTests.test_file_present_but_path_nonlist migrations.test_loader_llm.MigrationModuleClassificationTests.test_path_as_list_subclass_no_file migrations.test_loader_llm.MigrationModuleClassificationTests.test_regular_package_no_file_list_path migrations.test_loader_llm.MigrationModuleClassificationTests.test_spec_has_location_false_and_no_file_but_path_list
coverage json -o coverage.json
: '>>>>> End Test Output'
