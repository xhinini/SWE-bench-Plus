#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_formsets_llm.DuplicateCleanFormSet.clean forms_tests.tests.test_formsets_llm.NonFormErrorsRegressionTests.test_non_form_errors_identity_after_is_valid forms_tests.tests.test_formsets_llm.NonFormErrorsRegressionTests.test_non_form_errors_identity_on_bound_valid_formset forms_tests.tests.test_formsets_llm.NonFormErrorsRegressionTests.test_non_form_errors_on_unbound_formset_preserves_instance forms_tests.tests.test_formsets_llm.NonFormErrorsRegressionTests.test_non_form_errors_preserves_custom_error_class_instance forms_tests.tests.test_formsets_llm.NonFormErrorsRegressionTests.test_non_form_errors_repeated_calls_return_same_object forms_tests.tests.test_formsets_llm.NonFormErrorsRegressionTests.test_non_form_errors_return_type_is_errorlist_for_empty forms_tests.tests.test_formsets_llm.NonFormErrorsRegressionTests.test_non_form_errors_same_after_manual_full_clean
coverage json -o coverage.json
: '>>>>> End Test Output'
