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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 pagination.tests_llm.CountMethodContainer.__init__ pagination.tests_llm.CountMethodContainer.count pagination.tests_llm.IterationCountMethodTests.test_iter_with_count_method_container pagination.tests_llm.IterationRegressionTests.test_iter_independent_each_call pagination.tests_llm.IterationRegressionTests.test_iter_returns_page_objects pagination.tests_llm.IterationRegressionTests.test_iter_uses_get_page_hook_via__get_page_override pagination.tests_llm.IterationRegressionTests.test_iter_with_empty_object_list_and_allow_empty_first_page_false pagination.tests_llm.IterationRegressionTests.test_iteration_preserves_page_sequence_protocol pagination.tests_llm.WarningStackLevelRegressionTests.test_unordered_object_list_warning_points_to_caller
coverage json -o coverage.json
: '>>>>> End Test Output'
