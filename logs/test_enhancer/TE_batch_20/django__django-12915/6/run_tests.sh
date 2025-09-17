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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_handlers_llm.make_dummy staticfiles_tests.test_handlers_llm.make_request staticfiles_tests.test_handlers_llm.test__should_handle_false_when_base_url_has_netloc staticfiles_tests.test_handlers_llm.test__should_handle_true_when_path_under_base_and_no_netloc staticfiles_tests.test_handlers_llm.test_file_path_strips_base_url_and_converts staticfiles_tests.test_handlers_llm.test_get_response_async_handles_Http404_with_response_for_exception_in_thread staticfiles_tests.test_handlers_llm.test_get_response_async_propagates_non_Http404_exceptions staticfiles_tests.test_handlers_llm.test_get_response_async_propagates_response_for_exception_errors staticfiles_tests.test_handlers_llm.test_get_response_async_runs_serve_in_thread_success staticfiles_tests.test_handlers_llm.test_get_response_handles_Http404_synchronously staticfiles_tests.test_handlers_llm.test_get_response_uses_file_path_for_serve staticfiles_tests.test_handlers_llm.test_serve_passes_insecure_flag
coverage json -o coverage.json
: '>>>>> End Test Output'
