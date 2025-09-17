#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_state_llm.ProjectStateRealAppsTests.test_clone_preserves_real_apps_reference migrations.test_state_llm.ProjectStateRealAppsTests.test_real_apps_accepts_empty_set migrations.test_state_llm.ProjectStateRealAppsTests.test_real_apps_accepts_plain_set migrations.test_state_llm.ProjectStateRealAppsTests.test_real_apps_accepts_set_subclass migrations.test_state_llm.ProjectStateRealAppsTests.test_real_apps_allows_resolving_real_models migrations.test_state_llm.ProjectStateRealAppsTests.test_real_apps_defaults_to_empty_set migrations.test_state_llm.ProjectStateRealAppsTests.test_real_apps_rejects_frozenset migrations.test_state_llm.ProjectStateRealAppsTests.test_real_apps_rejects_generator_iterable migrations.test_state_llm.ProjectStateRealAppsTests.test_real_apps_rejects_list_iterable migrations.test_state_llm.ProjectStateRealAppsTests.test_real_apps_rejects_tuple_iterable
coverage json -o coverage.json
: '>>>>> End Test Output'
