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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_loader_llm.LoaderFilePathEdgeCasesTests._load_with_module migrations.test_loader_llm.LoaderFilePathEdgeCasesTests.test_already_loaded_package_without_file_and_list_path_is_loaded migrations.test_loader_llm.LoaderFilePathEdgeCasesTests.test_already_loaded_package_without_file_and_tuple_path_is_ignored migrations.test_loader_llm.LoaderFilePathEdgeCasesTests.test_package_without_file_and_custom_path_object_is_ignored migrations.test_loader_llm.LoaderFilePathEdgeCasesTests.test_package_without_file_and_list_path_is_loaded migrations.test_loader_llm.LoaderFilePathEdgeCasesTests.test_package_without_file_and_list_subclass_path_is_loaded migrations.test_loader_llm.LoaderFilePathEdgeCasesTests.test_package_without_file_and_tuple_path_is_ignored migrations.test_loader_llm.LoaderFilePathEdgeCasesTests.test_sysmodule_module_with_file_none_and_list_path_loaded migrations.test_loader_llm.LoaderFilePathEdgeCasesTests.test_sysmodule_module_with_file_none_and_tuple_path_ignored
coverage json -o coverage.json
: '>>>>> End Test Output'
