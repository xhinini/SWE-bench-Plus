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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_loader_llm.LoaderEdgeCaseTests._cleanup_package migrations.test_loader_llm.LoaderEdgeCaseTests._make_package migrations.test_loader_llm.LoaderEdgeCaseTests.test___path___is_list_subclass_still_recognised_as_package migrations.test_loader_llm.LoaderEdgeCaseTests.test_custom___path___object_iterable_is_treated_as_namespace migrations.test_loader_llm.LoaderEdgeCaseTests.test_custom___path___tuple_is_treated_as_namespace migrations.test_loader_llm.LoaderEdgeCaseTests.test_import_error_with_bad_magic_is_reworded migrations.test_loader_llm.LoaderEdgeCaseTests.test_migrations_as_module_file_are_ignored migrations.test_loader_llm.LoaderEdgeCaseTests.test_missing_Migration_class_raises_BadMigrationError migrations.test_loader_llm.LoaderEdgeCaseTests.test_namespace_package_without___init___is_ignored migrations.test_loader_llm.LoaderEdgeCaseTests.test_package_without___file___is_supported
coverage json -o coverage.json
: '>>>>> End Test Output'
