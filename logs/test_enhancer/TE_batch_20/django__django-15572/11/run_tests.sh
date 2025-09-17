#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 template_tests.test_autoreloader_llm.AutoreloadExtraTests._get_django_backend template_tests.test_autoreloader_llm.AutoreloadExtraTests.test_get_template_directories_ignores_empty_path_objects template_tests.test_autoreloader_llm.AutoreloadExtraTests.test_loader_get_dirs_empty_and_django_only_results_empty template_tests.test_autoreloader_llm.AutoreloadExtraTests.test_loader_get_dirs_ignores_django_path_entries template_tests.test_autoreloader_llm.AutoreloadExtraTests.test_multiple_backends_mixed_dirs_via_settings
coverage json -o coverage.json
: '>>>>> End Test Output'
