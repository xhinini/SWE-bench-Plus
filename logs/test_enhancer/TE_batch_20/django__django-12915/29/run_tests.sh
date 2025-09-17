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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_handlers_llm.DummyHandler.__init__ staticfiles_tests.test_handlers_llm.DummyHandler.serve staticfiles_tests.test_handlers_llm.GetResponseAsyncTests._fake_sync_to_async_factory staticfiles_tests.test_handlers_llm.GetResponseAsyncTests._make_request staticfiles_tests.test_handlers_llm.GetResponseAsyncTests.test_get_response_async_awaits_wrapped_function_asgi staticfiles_tests.test_handlers_llm.GetResponseAsyncTests.test_get_response_async_awaits_wrapped_function_dummy staticfiles_tests.test_handlers_llm.GetResponseAsyncTests.test_get_response_async_handles_non_response_return_value_dummy staticfiles_tests.test_handlers_llm.GetResponseAsyncTests.test_get_response_async_propagates_non_http404_exceptions_asgi staticfiles_tests.test_handlers_llm.GetResponseAsyncTests.test_get_response_async_propagates_non_http404_exceptions_dummy staticfiles_tests.test_handlers_llm.GetResponseAsyncTests.test_get_response_async_uses_sync_to_async_on_exception_asgi staticfiles_tests.test_handlers_llm.GetResponseAsyncTests.test_get_response_async_uses_sync_to_async_on_exception_dummy staticfiles_tests.test_handlers_llm.GetResponseAsyncTests.test_get_response_async_uses_sync_to_async_on_success_asgi staticfiles_tests.test_handlers_llm.GetResponseAsyncTests.test_get_response_async_uses_sync_to_async_on_success_dummy
coverage json -o coverage.json
: '>>>>> End Test Output'
