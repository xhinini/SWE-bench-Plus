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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 check_framework.test_translation_llm.TranslationConsistencyPatchTests.test_en_us_variant_handled check_framework.test_translation_llm.TranslationConsistencyPatchTests.test_get_supported_language_variant_called_once_for_valid_tag check_framework.test_translation_llm.TranslationConsistencyPatchTests.test_get_supported_language_variant_returning_canonical_value_still_returns_empty check_framework.test_translation_llm.TranslationConsistencyPatchTests.test_integer_language_code_calls_variant_and_returns_e004 check_framework.test_translation_llm.TranslationConsistencyPatchTests.test_invalid_language_get_supported_language_variant_raises_lookuperror check_framework.test_translation_llm.TranslationConsistencyPatchTests.test_non_lookuperror_exception_propagates check_framework.test_translation_llm.TranslationConsistencyPatchTests.test_none_language_get_supported_language_variant_raises_lookuperror check_framework.test_translation_llm.TranslationConsistencyPatchTests.test_unknown_language_tag_returns_e004 check_framework.test_translation_llm.TranslationConsistencyPatchTests.test_uppercase_language_code_handled check_framework.test_translation_llm.TranslationConsistencyPatchTests.test_valid_language_calls_get_supported_language_variant_and_returns_empty
coverage json -o coverage.json
: '>>>>> End Test Output'
