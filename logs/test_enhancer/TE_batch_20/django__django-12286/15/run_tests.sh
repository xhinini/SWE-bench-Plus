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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 check_framework.test_translation_llm.AdditionalTranslationConsistencyTests._run_with_patched_translation check_framework.test_translation_llm.AdditionalTranslationConsistencyTests.test_consistent_case_insensitive check_framework.test_translation_llm.AdditionalTranslationConsistencyTests.test_consistent_extlang check_framework.test_translation_llm.AdditionalTranslationConsistencyTests.test_consistent_fallback_to_primary check_framework.test_translation_llm.AdditionalTranslationConsistencyTests.test_consistent_long_variant check_framework.test_translation_llm.AdditionalTranslationConsistencyTests.test_consistent_numeric_region check_framework.test_translation_llm.AdditionalTranslationConsistencyTests.test_consistent_region_variant check_framework.test_translation_llm.AdditionalTranslationConsistencyTests.test_consistent_script check_framework.test_translation_llm.AdditionalTranslationConsistencyTests.test_consistent_simple_language check_framework.test_translation_llm.AdditionalTranslationConsistencyTests.test_consistent_three_letter_language check_framework.test_translation_llm.AdditionalTranslationConsistencyTests.test_consistent_with_en_us_alias
coverage json -o coverage.json
: '>>>>> End Test Output'
