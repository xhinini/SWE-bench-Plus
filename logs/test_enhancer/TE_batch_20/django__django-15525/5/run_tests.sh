#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.test_features_llm.BuildInstanceTests.test_handles_manager_get_by_natural_key_does_not_exist backends.sqlite.test_features_llm.BuildInstanceTests.test_multiple_calls_do_not_corrupt_data_dict_passed_in backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_can_use_instance_state_db backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_composed_of_multiple_values backends.sqlite.test_features_llm.BuildInstanceTests.test_sets_pk_using_natural_key_with_related_object backends.sqlite.test_features_llm.BuildInstanceTests.test_to_python_conversion_applied_to_manager_pk backends.sqlite.test_features_llm.BuildInstanceTests.test_uses_provided_db_when_querying_manager backends.sqlite.test_features_llm.DummyModel.__init__ backends.sqlite.test_features_llm.DummyModel.natural_key backends.sqlite.test_features_llm.DummyModelMeta.__init__ backends.sqlite.test_features_llm.DummyPK.__init__ backends.sqlite.test_features_llm.DummyPK.to_python backends.sqlite.test_features_llm.ManagerWithNaturalKey.__init__ backends.sqlite.test_features_llm.ManagerWithNaturalKey.db_manager backends.sqlite.test_features_llm.ManagerWithNaturalKey.db_used backends.sqlite.test_features_llm.ManagerWithNaturalKey.get_by_natural_key backends.sqlite.test_features_llm.[] (backends.sqlite.test_features_llm.DummyModel)
coverage json -o coverage.json
: '>>>>> End Test Output'
