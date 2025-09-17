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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_handlers_llm.DummyHandler.__init__ staticfiles_tests.test_handlers_llm.DummyHandler.serve staticfiles_tests.test_handlers_llm.DummyRequest.__init__ staticfiles_tests.test_handlers_llm.make_fake_sync_to_async staticfiles_tests.test_handlers_llm.test_get_response_async_called_for_each_concurrent_call staticfiles_tests.test_handlers_llm.test_get_response_async_calls_sync_to_async_on_http404 staticfiles_tests.test_handlers_llm.test_get_response_async_calls_sync_to_async_on_success staticfiles_tests.test_handlers_llm.test_get_response_async_does_not_call_response_for_exception_on_success staticfiles_tests.test_handlers_llm.test_get_response_async_passes_request_to_wrapped_function staticfiles_tests.test_handlers_llm.test_get_response_async_records_function_names staticfiles_tests.test_handlers_llm.test_get_response_async_returns_value_on_http404 staticfiles_tests.test_handlers_llm.test_get_response_async_returns_value_on_success staticfiles_tests.test_handlers_llm.test_get_response_async_wrapped_bound_method_preserves_self
coverage json -o coverage.json
: '>>>>> End Test Output'
