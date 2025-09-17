#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_forms_llm.PasswordHelpTextTests._extract_href auth_tests.test_forms_llm.PasswordHelpTextTests._password_help_text auth_tests.test_forms_llm.PasswordHelpTextTests.setUp auth_tests.test_forms_llm.PasswordHelpTextTests.test_urljoin_of_helptext_matches_password_change_url
coverage json -o coverage.json
: '>>>>> End Test Output'
