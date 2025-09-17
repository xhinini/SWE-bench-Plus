#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 template_tests.test_autoreloader_llm.GetTemplateDirectoriesRegressionTests._patch_djangotemplates template_tests.test_autoreloader_llm.GetTemplateDirectoriesRegressionTests._patch_engines_all template_tests.test_autoreloader_llm.GetTemplateDirectoriesRegressionTests.test_ignore_django_paths_from_loader_get_dirs template_tests.test_autoreloader_llm.MockDjangoTemplates.__init__ template_tests.test_autoreloader_llm.MockLoaderWithDirs.__init__ template_tests.test_autoreloader_llm.MockLoaderWithDirs.get_dirs template_tests.test_autoreloader_llm.MockLoaderWithDirs.reset template_tests.test_autoreloader_llm.MockLoaderWithoutGetDirs.__init__ template_tests.test_autoreloader_llm.MockLoaderWithoutGetDirs.reset
coverage json -o coverage.json
: '>>>>> End Test Output'
