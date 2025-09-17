#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 file_storage.test_models_llm._deconstruct_kwargs file_storage.test_models_llm.test_callable_class_storage_included_as_class file_storage.test_models_llm.test_callable_instance_storage_included file_storage.test_models_llm.test_callable_returning_default_included_as_callable file_storage.test_models_llm.test_callable_storage_included_as_callable file_storage.test_models_llm.test_custom_storage_instance_included file_storage.test_models_llm.test_default_storage_excluded file_storage.test_models_llm.test_instance_storage_included file_storage.test_models_llm.test_manual_storage_callable_set_to_default_storage_excluded file_storage.test_models_llm.test_max_length_default_removed file_storage.test_models_llm.test_pathlib_upload_to_preserved
coverage json -o coverage.json
: '>>>>> End Test Output'
