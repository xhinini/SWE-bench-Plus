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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_handlers_llm.DummyHandler.__init__ staticfiles_tests.test_handlers_llm.DummyRequest.__init__ staticfiles_tests.test_handlers_llm.test__should_handle_accepts_correct_prefix staticfiles_tests.test_handlers_llm.test__should_handle_ignores_host_in_base_url staticfiles_tests.test_handlers_llm.test_asgi_handler_init_does_not_call_super staticfiles_tests.test_handlers_llm.test_file_path_decodes_url_encoded_paths staticfiles_tests.test_handlers_llm.test_get_response_async_awaits_response_for_exception_call staticfiles_tests.test_handlers_llm.test_get_response_async_returns_same_as_get_response_for_success staticfiles_tests.test_handlers_llm.test_get_response_async_uses_sync_to_async_on_404 staticfiles_tests.test_handlers_llm.test_get_response_async_uses_sync_to_async_on_success staticfiles_tests.test_handlers_llm.test_get_response_sync_handles_404_calls_response_for_exception staticfiles_tests.test_handlers_llm.test_load_middleware_signature_has_no_extra_parameters
coverage json -o coverage.json
: '>>>>> End Test Output'
