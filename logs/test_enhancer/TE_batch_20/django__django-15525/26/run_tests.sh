#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.test_features_llm.Author.__init__ backends.sqlite.test_features_llm.Author.natural_key backends.sqlite.test_features_llm.Book.__init__ backends.sqlite.test_features_llm.Book.natural_key backends.sqlite.test_features_llm.BuildInstanceTests.test_db_forwarded_to_author_manager backends.sqlite.test_features_llm.BuildInstanceTests.test_missing_author_attribute_raises_attributeerror_in_gold_patch backends.sqlite.test_features_llm.BuildInstanceTests.test_multiple_field_types backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_with_related_instance_sets_pk backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_with_related_tuple_sets_pk_and_to_python backends.sqlite.test_features_llm.BuildInstanceTests.test_string_author_natural_key_sets_pk backends.sqlite.test_features_llm.BuildInstanceTests.test_to_python_conversion_returns_int backends.sqlite.test_features_llm.FakeManager.__init__ backends.sqlite.test_features_llm.FakeManager.db_manager backends.sqlite.test_features_llm.FakeMeta.__init__ backends.sqlite.test_features_llm.FakeMeta.get_field backends.sqlite.test_features_llm.FakePK.__init__ backends.sqlite.test_features_llm.FakePK.to_python backends.sqlite.test_features_llm.[] (backends.sqlite.test_features_llm.Author) backends.sqlite.test_features_llm.[] (backends.sqlite.test_features_llm.Book)
coverage json -o coverage.json
: '>>>>> End Test Output'
