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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_handlers_llm._bind_serve staticfiles_tests.test_handlers_llm._make_request staticfiles_tests.test_handlers_llm.test_get_response_async_concurrent_calls_run_concurrently staticfiles_tests.test_handlers_llm.test_get_response_async_does_not_block_event_loop_for_single_call staticfiles_tests.test_handlers_llm.test_get_response_async_handles_http404_in_different_thread staticfiles_tests.test_handlers_llm.test_get_response_async_immediate_return_runs_off_event_loop_thread staticfiles_tests.test_handlers_llm.test_get_response_async_multiple_concurrent_response_for_exception_calls staticfiles_tests.test_handlers_llm.test_get_response_async_propagates_non_http_exceptions staticfiles_tests.test_handlers_llm.test_get_response_async_response_for_exception_does_not_block_event_loop staticfiles_tests.test_handlers_llm.test_get_response_async_returns_value_and_threads_differ staticfiles_tests.test_handlers_llm.test_get_response_async_runs_serve_in_different_thread
coverage json -o coverage.json
: '>>>>> End Test Output'
