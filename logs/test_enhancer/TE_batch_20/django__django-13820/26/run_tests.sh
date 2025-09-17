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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_loader_llm.LoaderPathTypesTests.test_list_subclass_path_no_file_is_migrated migrations.test_loader_llm.LoaderPathTypesTests.test_regular_package_no_file_with_list_path_is_migrated migrations.test_loader_llm.LoaderPathTypesTests.test_regular_package_with_file_and_list_path_is_migrated migrations.test_loader_llm.LoaderPathTypesTests.test_tuple_path_with_file_is_namespace_and_unmigrated migrations.test_loader_llm.MockAppConfig.__init__ migrations.test_loader_llm._with_app_config
coverage json -o coverage.json
: '>>>>> End Test Output'
