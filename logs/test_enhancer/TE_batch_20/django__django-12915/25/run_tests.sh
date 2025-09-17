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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_handlers_llm.test__should_handle_respects_netloc staticfiles_tests.test_handlers_llm.test_file_path_strips_base_url_prefix_correctly staticfiles_tests.test_handlers_llm.test_file_path_uses_url2pathname_for_urlencoded_paths staticfiles_tests.test_handlers_llm.test_get_response_async_does_not_block_on_blocking_serve staticfiles_tests.test_handlers_llm.test_get_response_async_does_not_block_when_response_for_exception_blocks staticfiles_tests.test_handlers_llm.test_get_response_async_handles_http404_and_uses_response_for_exception staticfiles_tests.test_handlers_llm.test_get_response_async_returns_value_without_blocking_for_quick_serves staticfiles_tests.test_handlers_llm.test_multiple_concurrent_get_response_async_calls_are_parallel
coverage json -o coverage.json
: '>>>>> End Test Output'
