#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.test_alter_charfield_choices_noop_on_indexed_field schema.tests_llm.test_alter_charfield_choices_noop_variant schema.tests_llm.test_alter_field_choices_noop_on_index_from_meta_indexes schema.tests_llm.test_alter_field_choices_noop_preserves_indexes schema.tests_llm.test_alter_field_choices_noop_repeated schema.tests_llm.test_alter_field_choices_noop_with_generator_choices schema.tests_llm.test_alter_field_choices_noop_with_unique schema.tests_llm.test_alter_slugfield_choices_noop schema.tests_llm.test_alter_text_field_choices_noop_when_supported
coverage json -o coverage.json
: '>>>>> End Test Output'
