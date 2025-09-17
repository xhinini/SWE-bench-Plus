#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_formsets_llm.RegressionEmptyFormTests.test_empty_form_includes_custom_initial_from_get_form_kwargs forms_tests.tests.test_formsets_llm.RegressionEmptyFormTests.test_empty_form_with_all_conflicting_keys forms_tests.tests.test_formsets_llm.RegressionEmptyFormTests.test_empty_form_with_get_form_kwargs_auto_id_conflict forms_tests.tests.test_formsets_llm.RegressionEmptyFormTests.test_empty_form_with_get_form_kwargs_prefix_conflict forms_tests.tests.test_formsets_llm.RegressionEmptyFormTests.test_empty_form_with_get_form_kwargs_renderer_conflict forms_tests.tests.test_formsets_llm.RegressionEmptyFormTests.test_empty_form_with_get_form_kwargs_use_required_attribute_conflict
coverage json -o coverage.json
: '>>>>> End Test Output'
