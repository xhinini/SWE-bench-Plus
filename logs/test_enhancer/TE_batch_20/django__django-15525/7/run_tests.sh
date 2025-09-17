#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.test_features_llm.BuildInstanceTests.test_basic_related_natural_key_single_component backends.sqlite.test_features_llm.BuildInstanceTests.test_db_none_works_as_valid_db_argument backends.sqlite.test_features_llm.BuildInstanceTests.test_multiple_component_natural_key backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_raises_attributeerror_without_state_db backends.sqlite.test_features_llm.BuildInstanceTests.test_nested_natural_key_calls backends.sqlite.test_features_llm.BuildInstanceTests.test_non_string_natural_key_component backends.sqlite.test_features_llm.BuildInstanceTests.test_to_python_called_on_pk_string backends.sqlite.test_features_llm.BuildInstanceTests.test_uses_specified_db_not_default backends.sqlite.test_features_llm.BuildInstanceTests.test_varied_field_names_and_attnames backends.sqlite.test_features_llm.make_model
coverage json -o coverage.json
: '>>>>> End Test Output'
