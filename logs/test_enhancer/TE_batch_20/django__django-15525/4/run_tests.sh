#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.test_features_llm.BuildInstanceTests.test_db_alias_propagated_for_lookup backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_raises_if_db_not_set backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_uses_nested_related_attribute backends.sqlite.test_features_llm.BuildInstanceTests.test_sets_pk_and_uses_db_state backends.sqlite.test_features_llm.BuildInstanceTests.test_to_python_conversion_applied_to_pk backends.sqlite.test_features_llm.make_fake_model
coverage json -o coverage.json
: '>>>>> End Test Output'
