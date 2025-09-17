#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 template_tests.test_autoreloader_llm.DummyBackend.__init__ template_tests.test_autoreloader_llm.DummyLoader.__init__ template_tests.test_autoreloader_llm.DummyLoader.get_dirs template_tests.test_autoreloader_llm.DummyLoader.reset template_tests.test_autoreloader_llm.GetTemplateDirectoriesExtraTests._cleanup_patches template_tests.test_autoreloader_llm.GetTemplateDirectoriesExtraTests._patch_backend_and_engines template_tests.test_autoreloader_llm.GetTemplateDirectoriesExtraTests.setUp template_tests.test_autoreloader_llm.GetTemplateDirectoriesExtraTests.test_non_django_backend_ignored
coverage json -o coverage.json
: '>>>>> End Test Output'
