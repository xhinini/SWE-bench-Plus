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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 invalid_models_tests.test_relative_fields_llm.ManyToManyHintRegressionTests.test_ambiguous_relationship_model_from_class_through_defined_after_but_passed_as_class invalid_models_tests.test_relative_fields_llm.ManyToManyHintRegressionTests.test_ambiguous_relationship_model_from_class_through_defined_before invalid_models_tests.test_relative_fields_llm.ManyToManyHintRegressionTests.test_ambiguous_relationship_model_from_string_through_defined_after invalid_models_tests.test_relative_fields_llm.ManyToManyHintRegressionTests.test_ambiguous_relationship_model_from_string_through_with_different_name invalid_models_tests.test_relative_fields_llm.ManyToManyHintRegressionTests.test_ambiguous_relationship_model_to_class_through_defined_before invalid_models_tests.test_relative_fields_llm.ManyToManyHintRegressionTests.test_ambiguous_relationship_model_to_string_through_defined_after invalid_models_tests.test_relative_fields_llm.ManyToManyHintRegressionTests.test_ambiguous_relationship_model_to_string_through_defined_before_but_passed_as_class invalid_models_tests.test_relative_fields_llm.ManyToManyHintRegressionTests.test_ambiguous_relationship_model_to_string_with_custom_through_name
coverage json -o coverage.json
: '>>>>> End Test Output'
