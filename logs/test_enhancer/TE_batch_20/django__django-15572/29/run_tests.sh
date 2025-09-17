#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 template_tests.test_autoreloader_llm.FakeBackend.__init__ template_tests.test_autoreloader_llm.FakeLoader.__init__ template_tests.test_autoreloader_llm.FakeLoader.get_dirs template_tests.test_autoreloader_llm.FakeLoader.reset template_tests.test_autoreloader_llm.GetTemplateDirectoriesRegressionTests._with_fake_backend template_tests.test_autoreloader_llm.GetTemplateDirectoriesRegressionTests.test_loader_get_dirs_filters_django_paths template_tests.test_autoreloader_llm.GetTemplateDirectoriesRegressionTests.test_loader_get_dirs_ignores_mixed_falsy_and_django template_tests.test_autoreloader_llm.GetTemplateDirectoriesRegressionTests.test_pathlib_objects_in_dirs_are_handled
coverage json -o coverage.json
: '>>>>> End Test Output'
