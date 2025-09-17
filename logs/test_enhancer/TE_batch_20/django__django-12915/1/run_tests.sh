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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_handlers_llm.DummyRequest.__init__ staticfiles_tests.test_handlers_llm.test_get_response_async_concurrent_exception_and_success_threads_not_main staticfiles_tests.test_handlers_llm.test_get_response_async_handles_none_and_runs_in_thread staticfiles_tests.test_handlers_llm.test_get_response_async_multiple_calls_use_threadpool_threads_not_main staticfiles_tests.test_handlers_llm.test_get_response_async_multiple_invocations_threadpool_not_main staticfiles_tests.test_handlers_llm.test_get_response_async_non_http_exception_propagates_but_serve_ran_in_thread staticfiles_tests.test_handlers_llm.test_get_response_async_passes_request_to_serve_and_threaded staticfiles_tests.test_handlers_llm.test_get_response_async_response_for_exception_runs_in_thread_and_gets_args staticfiles_tests.test_handlers_llm.test_get_response_async_returns_value_from_serve_and_threaded staticfiles_tests.test_handlers_llm.test_get_response_async_runs_serve_in_thread_on_success staticfiles_tests.test_handlers_llm.test_get_response_async_runs_serve_in_thread_when_raises_http404
coverage json -o coverage.json
: '>>>>> End Test Output'
