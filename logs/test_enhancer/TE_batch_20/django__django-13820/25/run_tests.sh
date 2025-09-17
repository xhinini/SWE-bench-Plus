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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_loader_llm.LoaderPathTypeEdgeCasesTests._get_module_and_spec_backup migrations.test_loader_llm.LoaderPathTypeEdgeCasesTests._restore_module migrations.test_loader_llm.LoaderPathTypeEdgeCasesTests.test_custom_iterable_path_is_namespace migrations.test_loader_llm.LoaderPathTypeEdgeCasesTests.test_deque_path_is_namespace migrations.test_loader_llm.LoaderPathTypeEdgeCasesTests.test_proxy_path_object_is_namespace migrations.test_loader_llm.LoaderPathTypeEdgeCasesTests.test_tuple_path_with_no_file_is_namespace
coverage json -o coverage.json
: '>>>>> End Test Output'
