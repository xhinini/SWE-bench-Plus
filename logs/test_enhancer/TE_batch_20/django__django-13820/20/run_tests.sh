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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_loader_llm.FakeAppConfig.__init__ migrations.test_loader_llm.LoaderModuleShapeTests._make_migration_mod migrations.test_loader_llm.LoaderModuleShapeTests._make_pkg migrations.test_loader_llm.LoaderModuleShapeTests._setup_app_and_pkg migrations.test_loader_llm.LoaderModuleShapeTests.setUp migrations.test_loader_llm.LoaderModuleShapeTests.tearDown migrations.test_loader_llm.LoaderModuleShapeTests.test_bad_pyc_import_raises_helpful_error migrations.test_loader_llm.LoaderModuleShapeTests.test_custom_iterable_path_with_file_missing_but_file_present_migrated migrations.test_loader_llm.LoaderModuleShapeTests.test_ignored_filenames_are_skipped migrations.test_loader_llm.LoaderModuleShapeTests.test_list_subclass_path_with_no_file_is_migrated migrations.test_loader_llm.LoaderModuleShapeTests.test_missing_migration_class_raises_BadMigrationError migrations.test_loader_llm.LoaderModuleShapeTests.test_module_file_without_path_is_unmigrated migrations.test_loader_llm.LoaderModuleShapeTests.test_namespace_package_no_file_and_non_list_path_is_unmigrated migrations.test_loader_llm.LoaderModuleShapeTests.test_regular_package_no_file_but_list_path_is_migrated migrations.test_loader_llm.LoaderModuleShapeTests.test_regular_package_with_file_and_custom_path_obj_is_migrated
coverage json -o coverage.json
: '>>>>> End Test Output'
