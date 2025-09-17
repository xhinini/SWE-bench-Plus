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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_handlers_llm.test_get_response_async_called_concurrently staticfiles_tests.test_handlers_llm.test_get_response_async_does_not_detect_event_loop_inside_serve staticfiles_tests.test_handlers_llm.test_get_response_async_ensures_response_for_exception_called_in_threadpool staticfiles_tests.test_handlers_llm.test_get_response_async_exception_response_propagated staticfiles_tests.test_handlers_llm.test_get_response_async_handles_http404_in_thread staticfiles_tests.test_handlers_llm.test_get_response_async_response_value_propagated staticfiles_tests.test_handlers_llm.test_get_response_async_runs_serve_in_thread staticfiles_tests.test_handlers_llm.test_get_response_async_runs_serve_in_thread_multiple_calls staticfiles_tests.test_handlers_llm.test_get_response_async_with_bound_method staticfiles_tests.test_handlers_llm.test_get_response_async_with_lambda
coverage json -o coverage.json
: '>>>>> End Test Output'
