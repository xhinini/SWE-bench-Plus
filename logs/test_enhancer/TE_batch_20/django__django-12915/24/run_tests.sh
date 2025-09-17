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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_handlers_llm.DummyHandler.__init__ staticfiles_tests.test_handlers_llm.DummyHandler.serve staticfiles_tests.test_handlers_llm.test_get_response_async_awaits_coroutine_returned_by_sync_to_async staticfiles_tests.test_handlers_llm.test_get_response_async_calls_sync_to_async_on_exception_and_uses_response_for_exception staticfiles_tests.test_handlers_llm.test_get_response_async_calls_sync_to_async_on_success staticfiles_tests.test_handlers_llm.test_get_response_async_concurrent_calls_invoke_sync_to_async_each_time staticfiles_tests.test_handlers_llm.test_get_response_async_handles_non_awaitable_result_from_inner_coroutine staticfiles_tests.test_handlers_llm.test_get_response_async_handles_subclass_of_http404 staticfiles_tests.test_handlers_llm.test_get_response_async_only_wraps_serve_on_success staticfiles_tests.test_handlers_llm.test_get_response_async_passes_exception_instance_to_response_for_exception staticfiles_tests.test_handlers_llm.test_get_response_async_passes_request_argument_through staticfiles_tests.test_handlers_llm.test_get_response_async_returns_actual_response_object
coverage json -o coverage.json
: '>>>>> End Test Output'
