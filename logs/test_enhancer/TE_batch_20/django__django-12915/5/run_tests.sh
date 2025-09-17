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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_handlers_llm.DummyHandler.__init__ staticfiles_tests.test_handlers_llm.test_get_response_async_called_after_monkeypatching_back_original_sync_to_async staticfiles_tests.test_handlers_llm.test_get_response_async_called_multiple_times_uses_sync_to_async_each_time staticfiles_tests.test_handlers_llm.test_get_response_async_called_on_different_handler_instances staticfiles_tests.test_handlers_llm.test_get_response_async_does_not_suppress_errors_raised_by_response_for_exception_wrapper staticfiles_tests.test_handlers_llm.test_get_response_async_passes_request_to_wrapped_serve staticfiles_tests.test_handlers_llm.test_get_response_async_propagates_non_http404_and_uses_sync_to_async staticfiles_tests.test_handlers_llm.test_get_response_async_uses_sync_to_async_for_http404 staticfiles_tests.test_handlers_llm.test_get_response_async_uses_sync_to_async_on_success staticfiles_tests.test_handlers_llm.test_get_response_async_with_unusual_request_object staticfiles_tests.test_handlers_llm.test_get_response_async_wraps_response_for_exception
coverage json -o coverage.json
: '>>>>> End Test Output'
