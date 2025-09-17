#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_formsets_llm.RegressionEmptyFormTests.test_defaults_override_get_form_kwargs_values forms_tests.tests.test_formsets_llm.RegressionEmptyFormTests.test_empty_form_auto_id_conflict forms_tests.tests.test_formsets_llm.RegressionEmptyFormTests.test_empty_form_multiple_conflicts forms_tests.tests.test_formsets_llm.RegressionEmptyFormTests.test_empty_form_prefix_conflict forms_tests.tests.test_formsets_llm.RegressionEmptyFormTests.test_empty_form_renderer_conflict forms_tests.tests.test_formsets_llm.RegressionEmptyFormTests.test_empty_form_use_required_attribute_conflict forms_tests.tests.test_formsets_llm.RegressionEmptyFormTests.test_empty_permitted_conflict_ignored forms_tests.tests.test_formsets_llm.RegressionEmptyFormTests.test_get_form_kwargs_called_with_none_for_empty_form forms_tests.tests.test_formsets_llm.RegressionEmptyFormTests.test_preserve_custom_kwargs_on_empty_form
coverage json -o coverage.json
: '>>>>> End Test Output'
