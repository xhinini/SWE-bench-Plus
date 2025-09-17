#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.test_features_llm.BaseFakeModel.__init__ backends.sqlite.test_features_llm.BaseFakeModel._make_meta backends.sqlite.test_features_llm.BuildInstanceTests.test_calls_to_python_on_pk_conversion backends.sqlite.test_features_llm.BuildInstanceTests.test_handles_does_not_exist_from_get_by_natural_key backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_dependent_on_relation_attribute_set_by_init backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_iterable_is_passed_through_to_manager backends.sqlite.test_features_llm.BuildInstanceTests.test_propagates_attributeerror_from_natural_key backends.sqlite.test_features_llm.BuildInstanceTests.test_sets_state_db_before_natural_key_and_calls_manager backends.sqlite.test_features_llm.BuildInstanceTests.test_uses_provided_db_alias_variant backends.sqlite.test_features_llm.FakeDefaultManager.__init__ backends.sqlite.test_features_llm.FakeDefaultManager.db_manager backends.sqlite.test_features_llm.FakeManagerProxy.__init__ backends.sqlite.test_features_llm.FakeManagerProxy.get_by_natural_key backends.sqlite.test_features_llm.FakePK.__init__ backends.sqlite.test_features_llm.FakePK.to_python
coverage json -o coverage.json
: '>>>>> End Test Output'
