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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_handlers_llm.DummyHandler.__init__ staticfiles_tests.test_handlers_llm.test__should_handle_respects_netloc_in_base_url staticfiles_tests.test_handlers_llm.test_file_path_decodes_url_to_pathname staticfiles_tests.test_handlers_llm.test_get_response_async_calls_sync_to_async_exact_times_on_http404 staticfiles_tests.test_handlers_llm.test_get_response_async_calls_sync_to_async_exact_times_on_success staticfiles_tests.test_handlers_llm.test_get_response_async_calls_sync_to_async_for_http404_and_uses_response_for_exception staticfiles_tests.test_handlers_llm.test_get_response_async_calls_sync_to_async_for_success staticfiles_tests.test_handlers_llm.test_get_response_async_passes_request_argument_to_serve staticfiles_tests.test_handlers_llm.test_get_response_async_uses_wrapper_coroutine_when_awaited staticfiles_tests.test_handlers_llm.test_load_middleware_signature_not_changed
coverage json -o coverage.json
: '>>>>> End Test Output'
