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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_loader_llm.FakeAppConfig.__init__ migrations.test_loader_llm.MigrationLoaderPathTests._install_app_and_module migrations.test_loader_llm.MigrationLoaderPathTests._make_module migrations.test_loader_llm.MigrationLoaderPathTests.setUp migrations.test_loader_llm.MigrationLoaderPathTests.tearDown migrations.test_loader_llm.MigrationLoaderPathTests.test_complex_custom_path_object_with_list_behavior_but_not_list_is_namespace migrations.test_loader_llm.MigrationLoaderPathTests.test_deque___path___treated_as_namespace_package_and_ignored migrations.test_loader_llm.MigrationLoaderPathTests.test_list_subclass___path___treated_as_package_and_loads migrations.test_loader_llm.MigrationLoaderPathTests.test_missing___file___but_spec_has_location_false_and_list_path_loads migrations.test_loader_llm.MigrationLoaderPathTests.test_module_file_like_migrations_py_is_unmigrated migrations.test_loader_llm.MigrationLoaderPathTests.test_namespace_package_ignored_when_no___file___and_non_list___path__ migrations.test_loader_llm.MigrationLoaderPathTests.test_regular_package_without___file___loads_migrations migrations.test_loader_llm.MigrationLoaderPathTests.test_tuple___path___treated_as_namespace_package_and_ignored migrations.test_loader_llm.MigrationLoaderPathTests.test_was_loaded_triggers_reload_for_package
coverage json -o coverage.json
: '>>>>> End Test Output'
