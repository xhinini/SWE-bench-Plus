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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_handlers_llm.DummyHandler.__init__ staticfiles_tests.test_handlers_llm.make_recording_sync_to_async staticfiles_tests.test_handlers_llm.make_request staticfiles_tests.test_handlers_llm.test_get_response_async_async_serve_callable_is_still_wrapped_by_sync_to_async staticfiles_tests.test_handlers_llm.test_get_response_async_calls_sync_to_async_on_success staticfiles_tests.test_handlers_llm.test_get_response_async_does_not_call_response_for_exception_on_success staticfiles_tests.test_handlers_llm.test_get_response_async_propagates_non_http404_exceptions_and_still_uses_sync_to_async staticfiles_tests.test_handlers_llm.test_get_response_async_receives_correct_request_object_and_path staticfiles_tests.test_handlers_llm.test_get_response_async_records_wrapping_order_when_exception_then_response_for_exception staticfiles_tests.test_handlers_llm.test_get_response_async_uses_sync_to_async_for_http404_and_calls_response_for_exception staticfiles_tests.test_handlers_llm.test_multiple_consecutive_calls_record_all_sync_to_async_usages staticfiles_tests.test_handlers_llm.test_response_for_exception_arguments_are_preserved_through_sync_to_async_wrapper
coverage json -o coverage.json
: '>>>>> End Test Output'
