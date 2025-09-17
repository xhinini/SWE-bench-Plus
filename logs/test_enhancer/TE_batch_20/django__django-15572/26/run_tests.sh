#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 template_tests.test_autoreloader_llm.AdditionalTemplateReloadTests._make_backend template_tests.test_autoreloader_llm.AdditionalTemplateReloadTests._patch_engines_and_django_templates
coverage json -o coverage.json
: '>>>>> End Test Output'
