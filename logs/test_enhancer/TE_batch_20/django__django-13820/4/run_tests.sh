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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_loader_llm.AdditionalLoaderTests._cleanup_modules migrations.test_loader_llm.AdditionalLoaderTests._make_package_module migrations.test_loader_llm.AdditionalLoaderTests.test_bad_magic_number_import_error_wrapped migrations.test_loader_llm.AdditionalLoaderTests.test_ignore_files_prefixed_underscore_and_tilde migrations.test_loader_llm.AdditionalLoaderTests.test_list_subclass_path_treated_as_regular_package migrations.test_loader_llm.AdditionalLoaderTests.test_missing_migration_class_raises_BadMigrationError migrations.test_loader_llm.AdditionalLoaderTests.test_regular_package_no_file_with_list_path_is_migrated migrations.test_loader_llm.MockAppConfig.__init__
coverage json -o coverage.json
: '>>>>> End Test Output'
