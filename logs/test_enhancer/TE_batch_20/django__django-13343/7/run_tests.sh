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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 file_storage.tests_llm.FileFieldDeconstructTests.setUp file_storage.tests_llm.FileFieldDeconstructTests.tearDown file_storage.tests_llm.FileFieldDeconstructTests.test_deconstruct_callable_that_returns_default_storage_not_in_kwargs_even_if_callable_is_distinct file_storage.tests_llm.FileFieldDeconstructTests.test_deconstruct_omits_storage_when_callable_returns_default_storage file_storage.tests_llm.FileFieldDeconstructTests.test_deconstruct_omits_storage_when_lambda_returns_default_storage
coverage json -o coverage.json
: '>>>>> End Test Output'
