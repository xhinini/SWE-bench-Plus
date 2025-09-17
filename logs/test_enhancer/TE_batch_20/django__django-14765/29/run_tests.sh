#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_state_llm.RealAppsInitTests.test_clone_preserves_real_apps_identity migrations.test_state_llm.RealAppsInitTests.test_default_real_apps_is_empty_set migrations.test_state_llm.RealAppsInitTests.test_empty_set_real_apps_stays_empty migrations.test_state_llm.RealAppsInitTests.test_from_apps_default_real_apps_empty migrations.test_state_llm.RealAppsInitTests.test_invalid_app_label_in_real_apps_raises_lookup_error migrations.test_state_llm.RealAppsInitTests.test_real_apps_accepts_set_subclass migrations.test_state_llm.RealAppsInitTests.test_real_apps_accepts_set_with_valid_app migrations.test_state_llm.RealAppsInitTests.test_real_apps_rejects_frozenset migrations.test_state_llm.RealAppsInitTests.test_real_apps_rejects_list_type migrations.test_state_llm.RealAppsInitTests.test_real_apps_rejects_tuple_type
coverage json -o coverage.json
: '>>>>> End Test Output'
