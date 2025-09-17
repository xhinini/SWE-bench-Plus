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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_handlers_llm.DummyMixin.__init__ staticfiles_tests.test_handlers_llm.TestStaticFilesHandlers.test_asgi_handler_calls_application_for_non_http staticfiles_tests.test_handlers_llm.TestStaticFilesHandlers.test_get_response_async_handles_Http404_and_uses_sync_to_async staticfiles_tests.test_handlers_llm.TestStaticFilesHandlers.test_get_response_async_uses_sync_to_async_and_returns_result
coverage json -o coverage.json
: '>>>>> End Test Output'
