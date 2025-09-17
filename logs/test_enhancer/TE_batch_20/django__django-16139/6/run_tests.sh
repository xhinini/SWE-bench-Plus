#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_forms_llm.UserChangeFormPasswordLinkTests.setUp auth_tests.test_forms_llm.UserChangeFormPasswordLinkTests.test_href_can_be_joined_with_admin_change_url_to_get_password_change
coverage json -o coverage.json
: '>>>>> End Test Output'
