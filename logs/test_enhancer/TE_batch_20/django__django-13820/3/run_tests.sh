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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_loader_llm.AdditionalLoaderTests._setup_and_load migrations.test_loader_llm.AdditionalLoaderTests.setUp migrations.test_loader_llm.AdditionalLoaderTests.tearDown migrations.test_loader_llm.AdditionalLoaderTests.test_custom_path_with_file migrations.test_loader_llm.AdditionalLoaderTests.test_list_subclass_no_file migrations.test_loader_llm.AdditionalLoaderTests.test_multiple_apps_mixed migrations.test_loader_llm.AdditionalLoaderTests.test_regular_package_no_file migrations.test_loader_llm.AttrErrorModule.__getattribute__ migrations.test_loader_llm.EmptyIterable.__iter__ migrations.test_loader_llm.MockAppConfig.__init__
coverage json -o coverage.json
: '>>>>> End Test Output'
