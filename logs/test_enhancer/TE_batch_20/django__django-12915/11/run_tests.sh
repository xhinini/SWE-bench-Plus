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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_handlers_llm.test_get_response_async_can_be_called_repeatedly_quickly staticfiles_tests.test_handlers_llm.test_get_response_async_does_not_block_event_loop_when_serve_blocks staticfiles_tests.test_handlers_llm.test_get_response_async_preserves_request_argument_identity staticfiles_tests.test_handlers_llm.test_get_response_async_propagates_exception_from_response_for_exception staticfiles_tests.test_handlers_llm.test_get_response_async_propagates_non_http404_exception staticfiles_tests.test_handlers_llm.test_get_response_async_runs_serve_off_event_loop_and_returns staticfiles_tests.test_handlers_llm.test_get_response_async_uses_response_for_exception_off_event_loop_on_http404 staticfiles_tests.test_handlers_llm.test_get_response_sync_returns_and_handles_http404 staticfiles_tests.test_handlers_llm.test_multiple_concurrent_get_response_async_tasks_do_not_block_event_loop
coverage json -o coverage.json
: '>>>>> End Test Output'
