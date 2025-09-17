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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 invalid_models_tests.test_relative_fields_llm.HintRegressionTests.test_e334_hint_through_class_2 invalid_models_tests.test_relative_fields_llm.HintRegressionTests.test_e334_hint_through_class_4 invalid_models_tests.test_relative_fields_llm.HintRegressionTests.test_e334_hint_through_string_1 invalid_models_tests.test_relative_fields_llm.HintRegressionTests.test_e334_hint_through_string_3 invalid_models_tests.test_relative_fields_llm.HintRegressionTests.test_e334_hint_through_string_5 invalid_models_tests.test_relative_fields_llm.HintRegressionTests.test_e335_hint_through_class_2 invalid_models_tests.test_relative_fields_llm.HintRegressionTests.test_e335_hint_through_class_4 invalid_models_tests.test_relative_fields_llm.HintRegressionTests.test_e335_hint_through_string_1 invalid_models_tests.test_relative_fields_llm.HintRegressionTests.test_e335_hint_through_string_3
coverage json -o coverage.json
: '>>>>> End Test Output'
