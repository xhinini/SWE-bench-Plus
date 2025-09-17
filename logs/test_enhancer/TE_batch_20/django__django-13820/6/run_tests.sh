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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_loader_llm.LoaderEdgeCaseTests._make_module migrations.test_loader_llm.LoaderEdgeCaseTests.setUp migrations.test_loader_llm.LoaderEdgeCaseTests.test_custom_path_object_but_file_present_is_migrated migrations.test_loader_llm.LoaderEdgeCaseTests.test_path_tuple_but_file_present_is_migrated migrations.test_loader_llm.LoaderEdgeCaseTests.test_regular_package_with_no_file_and_path_list_is_migrated migrations.test_loader_llm.LoaderEdgeCaseTests.test_was_loaded_triggers_reload_and_marks_migrated_for_list_path migrations.test_loader_llm.MockAppConfig.__init__ migrations.test_loader_llm._cleanup_module migrations.test_loader_llm._install_fake_app_config migrations.test_loader_llm._restore_app_configs
coverage json -o coverage.json
: '>>>>> End Test Output'
