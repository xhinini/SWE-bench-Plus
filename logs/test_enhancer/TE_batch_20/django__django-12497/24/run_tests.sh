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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 invalid_models_tests.test_relative_fields_llm.ManyToManyHintTests.test_hint_ambiguous_from_class_through invalid_models_tests.test_relative_fields_llm.ManyToManyHintTests.test_hint_ambiguous_from_different_related_names invalid_models_tests.test_relative_fields_llm.ManyToManyHintTests.test_hint_ambiguous_from_string_through invalid_models_tests.test_relative_fields_llm.ManyToManyHintTests.test_hint_ambiguous_from_string_through_unrelated_names invalid_models_tests.test_relative_fields_llm.ManyToManyHintTests.test_hint_ambiguous_from_with_extra_field invalid_models_tests.test_relative_fields_llm.ManyToManyHintTests.test_hint_ambiguous_to_class_through invalid_models_tests.test_relative_fields_llm.ManyToManyHintTests.test_hint_ambiguous_to_string_through invalid_models_tests.test_relative_fields_llm.ManyToManyHintTests.test_hint_ambiguous_to_unqualified_names invalid_models_tests.test_relative_fields_llm.ManyToManyHintTests.test_hint_ambiguous_to_with_extra_field
coverage json -o coverage.json
: '>>>>> End Test Output'
