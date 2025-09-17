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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_loader_llm.LoaderNamespaceAndFileTests._run_with_module migrations.test_loader_llm.LoaderNamespaceAndFileTests.test_list_subclass_with_no_file_marked_migrated migrations.test_loader_llm.LoaderNamespaceAndFileTests.test_nonlist_path_but_with_file_marked_migrated migrations.test_loader_llm.LoaderNamespaceAndFileTests.test_package_with_path_list_and_file_marked_migrated migrations.test_loader_llm.LoaderNamespaceAndFileTests.test_package_with_path_list_no_file_marked_migrated
coverage json -o coverage.json
: '>>>>> End Test Output'
