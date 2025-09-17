#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_forms_llm.UserChangeFormPasswordLinkTests.setUp auth_tests.test_forms_llm.UserChangeFormPasswordLinkTests.test_admin_get_form_with_to_field_sets_helptext_with_pk auth_tests.test_forms_llm.UserChangeFormPasswordLinkTests.test_urljoin_behavior_with_base_without_trailing_slash
coverage json -o coverage.json
: '>>>>> End Test Output'
