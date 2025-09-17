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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_handlers_llm.DummyHandler.__init__ staticfiles_tests.test_handlers_llm.test_get_response_async_awaits_response_for_exception_return_value staticfiles_tests.test_handlers_llm.test_get_response_async_concurrent_calls_are_independent staticfiles_tests.test_handlers_llm.test_get_response_async_does_not_call_response_for_exception_when_no_exception staticfiles_tests.test_handlers_llm.test_get_response_async_handles_subclass_method_serve staticfiles_tests.test_handlers_llm.test_get_response_async_passes_exception_instance_to_response_for_exception staticfiles_tests.test_handlers_llm.test_get_response_async_propagates_non_http404_exceptions staticfiles_tests.test_handlers_llm.test_get_response_async_returns_serve_return_value staticfiles_tests.test_handlers_llm.test_get_response_async_runs_response_for_exception_in_thread_on_http404 staticfiles_tests.test_handlers_llm.test_get_response_async_runs_serve_in_thread_when_no_exception staticfiles_tests.test_handlers_llm.test_get_response_async_uses_sync_to_async_for_response_for_exception
coverage json -o coverage.json
: '>>>>> End Test Output'
