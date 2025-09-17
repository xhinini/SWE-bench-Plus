#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
export LANG=en_US.UTF-8
export LANGUAGE=en_US:en
export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf8
python --version && python -m pip install -U pip
python -m pip install -U 'coverage==6.2'

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldExtraTests.test_bound_data_returns_data_when_not_disabled auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldExtraTests.test_bound_data_with_empty_initial_when_not_disabled auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldExtraTests.test_has_changed_when_not_disabled auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldExtraTests.test_has_changed_with_empty_string_difference auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldExtraTests.test_has_changed_with_none_initial_and_nonempty_data_when_not_disabled auth_tests.test_forms_llm.ReadOnlyPasswordHashFieldExtraTests.test_integration_with_form_has_changed_respects_disabled_flag
coverage json -o coverage.json
: '>>>>> End Test Output'
