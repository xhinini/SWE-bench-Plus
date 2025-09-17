#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_views.test_adminsite_llm.BuildAppDictAttributeSimpleTests.test_private_build_method_name_is_private admin_views.test_adminsite_llm.BuildAppDictTests.setUp admin_views.test_adminsite_llm.BuildAppDictTests.setUpTestData admin_views.test_adminsite_llm.BuildAppDictTests.test_build_app_dict_filters_out_when_has_module_permission_false admin_views.test_adminsite_llm.BuildAppDictTests.test_build_app_dict_filters_out_when_no_true_permissions admin_views.test_adminsite_llm.BuildAppDictTests.test_build_app_dict_includes_model_key_for_all_apps admin_views.test_adminsite_llm.BuildAppDictTests.test_build_app_dict_with_label_returns_only_that_app admin_views.test_adminsite_llm.BuildAppDictTests.test_private_build_method_exists
coverage json -o coverage.json
: '>>>>> End Test Output'
