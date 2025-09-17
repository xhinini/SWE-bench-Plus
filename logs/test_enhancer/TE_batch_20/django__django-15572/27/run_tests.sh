#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 template_tests.test_autoreloader_llm.AdditionalTemplateAutoreloadTests.test_backend_dirs_handles_path_objects_and_ignores_empty_path template_tests.test_autoreloader_llm.AdditionalTemplateAutoreloadTests.test_loader_get_dirs_handles_path_objects_and_ignores_empty_path template_tests.test_autoreloader_llm._DummyBackend.__init__ template_tests.test_autoreloader_llm._DummyLoader.__init__ template_tests.test_autoreloader_llm._DummyLoader.get_dirs template_tests.test_autoreloader_llm._DummyLoader.reset
coverage json -o coverage.json
: '>>>>> End Test Output'
