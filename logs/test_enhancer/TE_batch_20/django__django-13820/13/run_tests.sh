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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_loader_llm.LoaderNamespacePackageTests._insert_module migrations.test_loader_llm.LoaderNamespacePackageTests._make_app_config migrations.test_loader_llm.LoaderNamespacePackageTests._remove_module migrations.test_loader_llm.LoaderNamespacePackageTests.test_list_subclass_path_accepted_without_file migrations.test_loader_llm.LoaderNamespacePackageTests.test_package_with_file_and_list_path_accepted migrations.test_loader_llm.LoaderNamespacePackageTests.test_package_with_file_and_nonlist_path_accepted migrations.test_loader_llm.LoaderNamespacePackageTests.test_regular_package_no_file_path_list_accepted
coverage json -o coverage.json
: '>>>>> End Test Output'
