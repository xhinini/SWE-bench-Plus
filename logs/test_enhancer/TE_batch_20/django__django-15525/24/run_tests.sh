#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.test_features_llm.BaseFakeModel.__init__ backends.sqlite.test_features_llm.BaseFakeModel.__repr__ backends.sqlite.test_features_llm.DummyState.__init__ backends.sqlite.test_features_llm.SimpleManager.__init__ backends.sqlite.test_features_llm.SimpleManager.db_manager backends.sqlite.test_features_llm.SimpleManager.get_by_natural_key backends.sqlite.test_features_llm.SimpleManager.marker backends.sqlite.test_features_llm.TestBuildInstance.test_candidate_patch_fails_to_set_remote_fields_affecting_natural_key backends.sqlite.test_features_llm.TestBuildInstance.test_natural_key_requires_state_db_raises_without_it_but_fixed_by_patch backends.sqlite.test_features_llm.TestBuildInstance.test_resolve_natural_key_uses_state_db backends.sqlite.test_features_llm.TestBuildInstance.test_to_python_conversion_applied backends.sqlite.test_features_llm.make_meta
coverage json -o coverage.json
: '>>>>> End Test Output'
