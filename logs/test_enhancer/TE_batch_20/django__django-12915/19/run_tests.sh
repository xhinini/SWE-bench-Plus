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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_handlers_llm.DummyHandler.__init__ staticfiles_tests.test_handlers_llm.test__should_handle_accepts_exact_base_path_equal staticfiles_tests.test_handlers_llm.test__should_handle_respects_netloc staticfiles_tests.test_handlers_llm.test_file_path_decodes_percent_encoding staticfiles_tests.test_handlers_llm.test_file_path_empty_relative staticfiles_tests.test_handlers_llm.test_get_base_url_checks_settings staticfiles_tests.test_handlers_llm.test_get_response_async_handles_exception_without_blocking staticfiles_tests.test_handlers_llm.test_get_response_async_returns_response_when_not_404 staticfiles_tests.test_handlers_llm.test_get_response_async_runs_serve_in_thread staticfiles_tests.test_handlers_llm.test_get_response_returns_response_for_exception_sync staticfiles_tests.test_handlers_llm.test_serve_calls_module_serve_with_insecure_flag
coverage json -o coverage.json
: '>>>>> End Test Output'
