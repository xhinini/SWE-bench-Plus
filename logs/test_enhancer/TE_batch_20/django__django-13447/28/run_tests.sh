#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_views.test_adminsite_llm.BuildAppDictTests.setUp admin_views.test_adminsite_llm.BuildAppDictTests.setUpTestData admin_views.test_adminsite_llm.BuildAppDictTests.test__build_app_dict_method_exists_and_callable admin_views.test_adminsite_llm.BuildAppDictTests.test__build_app_dict_returns_apps_and_models_include_model_key admin_views.test_adminsite_llm.BuildAppDictTests.test__build_app_dict_unknown_label_returns_none admin_views.test_adminsite_llm.BuildAppDictTests.test__build_app_dict_with_label_returns_only_that_app admin_views.test_adminsite_llm.BuildAppDictTests.test_auth_user_model_has_admin_and_add_urls_and_model_key admin_views.test_adminsite_llm.BuildAppDictTests.test_model_entry_has_expected_fields admin_views.test_adminsite_llm.BuildAppDictTests.test_new_adminsite_with_no_models_returns_empty_dict
coverage json -o coverage.json
: '>>>>> End Test Output'
