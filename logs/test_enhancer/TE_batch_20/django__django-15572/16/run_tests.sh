#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 template_tests.test_autoreloader_llm.MockLoader.__init__ template_tests.test_autoreloader_llm.MockLoader.get_dirs template_tests.test_autoreloader_llm.TemplateAutoreloadNewTests._make_backend template_tests.test_autoreloader_llm.TemplateAutoreloadNewTests.test_get_template_directories_filters_out_django_loader_paths
coverage json -o coverage.json
: '>>>>> End Test Output'
