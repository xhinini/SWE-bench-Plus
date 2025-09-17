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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_loader_llm.FakeMigrationModule.__init__ migrations.test_loader_llm.MigrationLoaderPathTypeTests._cleanup_modules migrations.test_loader_llm.MigrationLoaderPathTypeTests._make_package migrations.test_loader_llm.MigrationLoaderPathTypeTests.setUp migrations.test_loader_llm.MigrationLoaderPathTypeTests.test_existing_module_reload_called_when_preloaded migrations.test_loader_llm.MigrationLoaderPathTypeTests.test_file_present_with_custom_path_loads migrations.test_loader_llm.MigrationLoaderPathTypeTests.test_list_subclass_path_is_loaded migrations.test_loader_llm.MigrationLoaderPathTypeTests.test_regular_package_without_file_and_list_path_is_loaded
coverage json -o coverage.json
: '>>>>> End Test Output'
