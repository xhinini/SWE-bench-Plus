#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 template_tests.test_autoreloader_llm.GetTemplateDirectoriesMockingTests._run_with_backend template_tests.test_autoreloader_llm.GetTemplateDirectoriesMockingTests.test_is_django_path_case_sensitivity template_tests.test_autoreloader_llm.GetTemplateDirectoriesMockingTests.test_loader_filters_django_path_and_keeps_valid template_tests.test_autoreloader_llm._LoaderWithGetDirs.__init__ template_tests.test_autoreloader_llm._LoaderWithGetDirs.get_dirs template_tests.test_autoreloader_llm._MockTemplateBackend.__init__
coverage json -o coverage.json
: '>>>>> End Test Output'
