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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_loader_llm.FakeAppConfig.__init__ migrations.test_loader_llm.LoaderModuleClassificationTests._run_with_module migrations.test_loader_llm.LoaderModuleClassificationTests.setUp migrations.test_loader_llm.LoaderModuleClassificationTests.tearDown migrations.test_loader_llm.LoaderModuleClassificationTests.test_package_with___path__as_list_subclass_is_migrated migrations.test_loader_llm.LoaderModuleClassificationTests.test_package_with__file__present_and_path_not_list_is_migrated_if_package migrations.test_loader_llm.LoaderModuleClassificationTests.test_regular_package_without___file___is_migrated migrations.test_loader_llm.LoaderModuleClassificationTests.test_reload_called_if_already_loaded_and_package_is_valid
coverage json -o coverage.json
: '>>>>> End Test Output'
