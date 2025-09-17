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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_text_llm.test_slugify_collapse_then_strip utils_tests.test_text_llm.test_slugify_mixed_edge_chars utils_tests.test_text_llm.test_slugify_preserve_internal_underscores utils_tests.test_text_llm.test_slugify_spaces_underscores_and_chars utils_tests.test_text_llm.test_slugify_strip_leading_trailing_mix utils_tests.test_text_llm.test_slugify_strip_leading_trailing_underscores utils_tests.test_text_llm.test_slugify_strip_only_dashes utils_tests.test_text_llm.test_slugify_strip_only_spaces utils_tests.test_text_llm.test_slugify_strip_only_underscores utils_tests.test_text_llm.test_slugify_strip_spaces_and_dashes
coverage json -o coverage.json
: '>>>>> End Test Output'
