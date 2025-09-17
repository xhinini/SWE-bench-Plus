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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_handlers_llm.DummyHandler.__init__ staticfiles_tests.test_handlers_llm.DummyHandler.serve staticfiles_tests.test_handlers_llm.test_get_response_async_concurrent_calls_all_use_threadpool staticfiles_tests.test_handlers_llm.test_get_response_async_exception_path_preserves_exception_instance staticfiles_tests.test_handlers_llm.test_get_response_async_multiple_exception_calls_dont_share_state staticfiles_tests.test_handlers_llm.test_get_response_async_propagates_non_http404_exceptions staticfiles_tests.test_handlers_llm.test_get_response_async_response_for_exception_receives_arguments_in_threadpool staticfiles_tests.test_handlers_llm.test_get_response_async_runs_response_for_exception_in_thread_on_http404 staticfiles_tests.test_handlers_llm.test_get_response_async_runs_serve_in_thread_different_thread_for_success staticfiles_tests.test_handlers_llm.test_get_response_async_sequential_calls_all_use_threadpool staticfiles_tests.test_handlers_llm.test_get_response_async_with_blocking_serve_does_not_block_event_loop staticfiles_tests.test_handlers_llm.test_get_response_async_works_with_dummy_request_objects
coverage json -o coverage.json
: '>>>>> End Test Output'
