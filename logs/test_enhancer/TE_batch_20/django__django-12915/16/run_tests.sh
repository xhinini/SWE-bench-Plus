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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_handlers_llm.DummyHandler.__init__ staticfiles_tests.test_handlers_llm.DummyHandler.serve staticfiles_tests.test_handlers_llm.DummyRequest.__init__ staticfiles_tests.test_handlers_llm.test_event_loop_not_blocked_by_blocking_serve staticfiles_tests.test_handlers_llm.test_get_response_async_returns_serve_result staticfiles_tests.test_handlers_llm.test_multiple_concurrent_get_response_async_calls staticfiles_tests.test_handlers_llm.test_non_http404_exception_propagates staticfiles_tests.test_handlers_llm.test_response_for_exception_runs_outside_event_loop_on_404 staticfiles_tests.test_handlers_llm.test_serve_called_outside_event_loop_with_bound_method_identity staticfiles_tests.test_handlers_llm.test_serve_runs_outside_event_loop staticfiles_tests.test_handlers_llm.test_sync_to_async_is_used_for_response_for_exception_on_404 staticfiles_tests.test_handlers_llm.test_sync_to_async_is_used_for_serve staticfiles_tests.test_handlers_llm.test_sync_to_async_wrapper_called_for_both_functions
coverage json -o coverage.json
: '>>>>> End Test Output'
