#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 file_storage.test_models_llm.test_deconstruct_includes_callable_returning_custom_storage file_storage.test_models_llm.test_deconstruct_includes_callable_returning_default_storage file_storage.test_models_llm.test_deconstruct_includes_callable_storage_class file_storage.test_models_llm.test_deconstruct_includes_custom_storage_instance file_storage.test_models_llm.test_deconstruct_includes_upload_to_callable file_storage.test_models_llm.test_deconstruct_includes_upload_to_pathlib file_storage.test_models_llm.test_deconstruct_includes_upload_to_string file_storage.test_models_llm.test_deconstruct_keeps_nondefault_max_length file_storage.test_models_llm.test_deconstruct_omits_default_storage_instance file_storage.test_models_llm.test_deconstruct_removes_default_max_length
coverage json -o coverage.json
: '>>>>> End Test Output'
