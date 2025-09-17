#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_views.test_adminsite_llm.AdminSiteBuildAppDictTests.setUp admin_views.test_adminsite_llm.AdminSiteBuildAppDictTests.setUpTestData admin_views.test_adminsite_llm.AdminSiteBuildAppDictTests.test__build_app_dict_attribute_exists_and_callable admin_views.test_adminsite_llm.AdminSiteBuildAppDictTests.test__build_app_dict_excludes_models_without_perms admin_views.test_adminsite_llm.AdminSiteBuildAppDictTests.test__build_app_dict_returns_models_with_model_key admin_views.test_adminsite_llm.AdminSiteBuildAppDictTests.test__build_app_dict_with_label_returns_single_app_dict
coverage json -o coverage.json
: '>>>>> End Test Output'
