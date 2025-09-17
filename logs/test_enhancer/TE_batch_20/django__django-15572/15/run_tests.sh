#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 template_tests.test_autoreloader_llm.AdditionalTemplateReloadTests.test_get_template_directories_ignores_pathlike_empty_entry template_tests.test_autoreloader_llm.AdditionalTemplateReloadTests.test_loader_get_dirs_ignores_django_package_paths template_tests.test_autoreloader_llm._Loader.__init__ template_tests.test_autoreloader_llm._Loader.get_dirs template_tests.test_autoreloader_llm._Loader.reset
coverage json -o coverage.json
: '>>>>> End Test Output'
