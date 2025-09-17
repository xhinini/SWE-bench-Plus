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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_handlers_llm.DummyRequest.__init__ staticfiles_tests.test_handlers_llm.make_fake_sync_to_async staticfiles_tests.test_handlers_llm.make_handler staticfiles_tests.test_handlers_llm.test_get_response_async_calls_sync_to_async_on_success staticfiles_tests.test_handlers_llm.test_get_response_async_calls_sync_to_async_twice_on_404 staticfiles_tests.test_handlers_llm.test_get_response_async_handles_http404_via_response_for_exception staticfiles_tests.test_handlers_llm.test_get_response_async_multiple_calls_each_calls_sync_to_async staticfiles_tests.test_handlers_llm.test_get_response_async_passes_request_arg_and_returns_value staticfiles_tests.test_handlers_llm.test_get_response_async_propagates_non_http404_exceptions_and_uses_sync_to_async staticfiles_tests.test_handlers_llm.test_get_response_async_response_for_exception_called_with_correct_args staticfiles_tests.test_handlers_llm.test_get_response_async_with_bound_method_identity staticfiles_tests.test_handlers_llm.test_get_response_async_with_different_request_objects
coverage json -o coverage.json
: '>>>>> End Test Output'
